from odoo import models, fields, api
from odoo.exceptions import UserError  # Importar UserError

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

    @api.depends('lineas_venta.subtotal')
    def _calcular_total(self):
        for record in self:
            record.total = sum(linea.subtotal for linea in record.lineas_venta)

    def action_confirmar(self):
        """Confirma la venta y reduce el stock de los suplementos."""
        for record in self:
            for linea in record.lineas_venta:
                if linea.suplemento_id.stock < linea.cantidad:
                    # Mostrar un mensaje de error más claro al usuario
                    raise UserError(
                        f"🚨 No hay suficiente stock para '{linea.suplemento_id.name}'.\n\n"
                        f"📦 Stock disponible: {linea.suplemento_id.stock}\n"
                        f"❗ Cantidad solicitada: {linea.cantidad}\n\n"
                        "Por favor, ajusta la cantidad antes de confirmar la venta."
                    )
                # Si hay suficiente stock, reduce la cantidad
                linea.suplemento_id.stock -= linea.cantidad
            record.estado = "confirmado"


    def action_cancelar(self):
        """ Cancela la venta, restablece el stock """
        for record in self:
            for linea in record.lineas_venta:
                linea.suplemento_id.stock += linea.cantidad
            record.estado = "cancelado"
