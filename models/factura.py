from odoo import models, fields, api

class Factura(models.Model):
    _name = "factura.model"
    _description = "Factura de Venta"

    name = fields.Char("Número de Factura", required=True, copy=False, readonly=True, default="New")
    venta_id = fields.Many2one("venta.model", string="Venta Relacionada", readonly=True, ondelete="cascade")
    cliente_id = fields.Many2one("cliente.model", string="Cliente", required=True)
    fecha_factura = fields.Date("Fecha de Factura", default=fields.Date.context_today)
    total = fields.Float("Total", compute="_calcular_total", store=True)
    estado = fields.Selection([
        ("borrador", "Borrador"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ], string="Estado", default="borrador")
    lineas_factura = fields.One2many("facturalinea.model", "factura_id", string="Líneas de Factura")

    @api.depends("lineas_factura.subtotal")
    def _calcular_total(self):
        for factura in self:
            factura.total = sum(linea.subtotal for linea in factura.lineas_factura)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('factura.model') or 'New'
        return super(Factura, self).create(vals)

    def action_pagar(self):
        """Marca la factura como pagada"""
        self.write({"estado": "pagado"})

    def action_cancelar(self):
        """Cancela la factura"""
        self.write({"estado": "cancelado"})
