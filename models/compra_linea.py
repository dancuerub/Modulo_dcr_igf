from odoo import models, fields, api

class CompraLinea(models.Model):
    _name = 'compralinea.model'
    _description = 'Líneas de Compra'

    compra_id = fields.Many2one('compra.model', string='Compra', required=True, ondelete='cascade')
    suplemento_id = fields.Many2one('suplemento.model', string='Suplemento', required=True, domain="[('proveedor_id', '!=', False)]")
    cantidad = fields.Integer('Cantidad', required=True, default=1)
    precio_unitario = fields.Float('Precio Unitario', related='suplemento_id.precio_compra', store=True)
    subtotal = fields.Float('Subtotal', compute='_calcular_subtotal', store=True)

    @api.depends('cantidad', 'precio_unitario')
    def _calcular_subtotal(self):
        for linea in self:
            linea.subtotal = linea.cantidad * linea.precio_unitario