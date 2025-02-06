from odoo import models, fields, api

class FacturaCompraLinea(models.Model):
    _name = "facturacompralinea.model"
    _description = "Línea de Factura de Compra"

    factura_compra_id = fields.Many2one("facturacompra.model", string="Factura de Compra", required=True, ondelete="cascade")
    suplemento_id = fields.Many2one("suplemento.model", string="Suplemento", required=True)
    cantidad = fields.Integer("Cantidad", required=True, default=1)
    precio_unitario = fields.Float("Precio Unitario", required=True)
    subtotal = fields.Float("Subtotal", compute="_calcular_subtotal", store=True)

    @api.depends("cantidad", "precio_unitario")
    def _calcular_subtotal(self):
        for linea in self:
            linea.subtotal = linea.cantidad * linea.precio_unitario
