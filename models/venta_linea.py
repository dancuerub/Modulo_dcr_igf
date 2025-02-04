from odoo import models, fields, api

class VentaLinea(models.Model):
    _name = "ventalinea.model"
    _description = "Línea de Venta"

    venta_id = fields.Many2one('venta.model', string="Venta", required=True, ondelete='cascade')
    suplemento_id = fields.Many2one('suplemento.model', string="Suplemento", required=True)
    cantidad = fields.Integer("Cantidad", required=True, default=1)
    precio_unitario = fields.Float("Precio Unitario", related="suplemento_id.precio_venta", store=True)
    subtotal = fields.Float("Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.cantidad * record.precio_unitario
