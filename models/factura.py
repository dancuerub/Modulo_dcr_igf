from odoo import models, fields, api

class Factura(models.Model):
    _name = "factura.model"
    _description = "Factura de Venta"

    name = fields.Char("Número de Factura", required=True, copy=False, readonly=True, default="New")
    venta_id = fields.Many2one("venta.model", string="Venta Relacionada", readonly=True, ondelete="cascade")
    cliente_id = fields.Many2one("cliente.model", string="Cliente", required=True)
    fecha_factura = fields.Date("Fecha de Factura", default=fields.Date.context_today)
    total = fields.Float("Total", compute="_calcular_total", store=True)
    lineas_factura = fields.One2many("facturalinea.model", "factura_id", readonly=True, string="Líneas de Factura")

    @api.depends("lineas_factura.subtotal")
    def _calcular_total(self):
        for factura in self:
            factura.total = round(sum(linea.subtotal for linea in factura.lineas_factura), 2)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('factura.model') or 'New'
        return super(Factura, self).create(vals)

    def action_imprimir_factura(self):
        """Genera y descarga la factura en PDF."""
        return self.env.ref('suplementos.action_reporte_factura').report_action(self)
