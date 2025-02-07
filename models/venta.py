from odoo import models, fields, api
from odoo.exceptions import UserError

class Venta(models.Model):
    _name = "venta.model"
    _description = "Gestión de Ventas"

    name = fields.Char("Referencia", required=True, copy=False, readonly=True, default="New")
    cliente_id = fields.Many2one('cliente.model', string="Cliente", required=True)
    fecha_venta = fields.Date("Fecha de Venta", default=fields.Date.context_today)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ], string="Estado", default="borrador")
    total = fields.Float("Total", compute="_calcular_total", store=True)
    lineas_venta = fields.One2many('ventalinea.model', 'venta_id', string="Líneas de Venta")
    factura_id = fields.Many2one('factura.model', string="Factura Generada", readonly=True)

    @api.depends('lineas_venta.subtotal')
    def _calcular_total(self):
        for record in self:
            record.total = round(sum(linea.subtotal for linea in record.lineas_venta), 2)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('venta.model') or 'New'
        return super(Venta, self).create(vals)

    def action_confirmar(self):
        """Confirma la venta, reduce stock y genera la factura."""
        for record in self:

            # Validar stock
            for linea in record.lineas_venta:
                if linea.suplemento_id.stock < linea.cantidad:
                    raise UserError(
                        f"🚨 No hay suficiente stock para '{linea.suplemento_id.name}'.\n\n"
                        f"📦 Stock disponible: {linea.suplemento_id.stock}\n"
                        f"❗ Cantidad solicitada: {linea.cantidad}\n\n"
                        "Por favor, ajusta la cantidad antes de confirmar la venta."
                    )
                # Reducir stock
                linea.suplemento_id.stock -= linea.cantidad
            
            # Crear factura
            factura_vals = {
                "venta_id": record.id,
                "cliente_id": record.cliente_id.id,
                "fecha_factura": fields.Date.context_today(self),
                "lineas_factura": [(0, 0, {
                    "suplemento_id": linea.suplemento_id.id,
                    "cantidad": linea.cantidad,
                    "precio_unitario": linea.precio_unitario,
                    "subtotal": linea.subtotal,
                }) for linea in record.lineas_venta],
            }
            factura = self.env["factura.model"].create(factura_vals)
            record.factura_id = factura.id

            # Cambiar estado de la venta
            record.estado = "confirmado"

    def action_cancelar(self):
        """Cancela la venta, restablece el stock y cancela la factura."""
        for record in self:
            for linea in record.lineas_venta:
                linea.suplemento_id.stock += linea.cantidad
            
            # Si hay una factura generada, se cancela
            if record.factura_id:
                record.factura_id.action_cancelar()

            record.estado = "cancelado"
