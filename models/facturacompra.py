from odoo import models, fields, api

class FacturaCompra(models.Model):
    _name = "facturacompra.model"
    _description = "Factura de Compra"

    name = fields.Char("Número de Factura", required=True, copy=False, readonly=True, default="New")
    compra_id = fields.Many2one("compra.model", string="Compra Relacionada", readonly=True)
    proveedor_id = fields.Many2one("proveedor.model", string="Proveedor", required=True)
    fecha_factura = fields.Date("Fecha de Factura", default=fields.Date.context_today)
    total = fields.Float("Total", compute="_calcular_total", store=True)
    lineas_factura = fields.One2many("facturacompralinea.model", "factura_compra_id", readonly=True, string="Líneas de Factura")

    @api.depends("lineas_factura.subtotal")
    def _calcular_total(self):
        for factura in self:
            factura.total = round(sum(linea.subtotal for linea in factura.lineas_factura), 2)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('facturacompra.model') or 'New'
        return super(FacturaCompra, self).create(vals)

    def action_imprimir_factura(self):
        """Genera y descarga la factura en PDF."""
        return self.env.ref('suplementos.action_reporte_factura_compra').report_action(self)
