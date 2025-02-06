from odoo import models, fields, api

class Compra(models.Model):
    _name = 'compra.model'
    _description = 'Registro de Compras a Proveedores'

    name = fields.Char('Referencia de Compra', required=True, copy=False, readonly=True, 
    default='Nuevo')
    proveedor_id = fields.Many2one('proveedor.model', string='Proveedor', required=True)
    fecha_compra = fields.Date('Fecha de Compra', default=fields.Date.today, required=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='borrador')

    lineas_compra = fields.One2many('compralinea.model', 'compra_id', string='Líneas de Compra')
    factura_id = fields.Many2one('facturacompra.model', string="Factura Generada", readonly=True)

    total = fields.Float('Total', compute='_calcular_total', store=True)

    @api.depends('lineas_compra.subtotal')
    def _calcular_total(self):
        for compra in self:
            compra.total = sum(linea.subtotal for linea in compra.lineas_compra)

    def confirmar_compra(self):
        """ Método para confirmar la compra """
        for compra in self:
            compra.estado = 'confirmado'

    def recibir_compra(self):
        """ Método para recibir la compra y sumar stock y generar factura """
        for compra in self:
            if compra.estado == 'confirmado':
                # Aumentamos el stock de cada línea de compra
                for linea in compra.lineas_compra:
                    linea.suplemento_id.stock += linea.cantidad
                
                # Crear la factura de compra automáticamente
                factura_vals = {
                    "compra_id": compra.id,
                    "proveedor_id": compra.proveedor_id.id,
                    "fecha_factura": fields.Date.today(),
                    "lineas_factura": [(0, 0, {
                        "suplemento_id": linea.suplemento_id.id,
                        "cantidad": linea.cantidad,
                        "precio_unitario": linea.precio_unitario,
                        "subtotal": linea.subtotal,
                    }) for linea in compra.lineas_compra],
                }
                factura = self.env["facturacompra.model"].create(factura_vals)
                compra.factura_id = factura.id

                # Cambiamos el estado de la compra a 'recibido'
                compra.estado = 'recibido'

    def cancelar_compra(self):
        """ Método para cancelar la compra """
        for compra in self:
            compra.estado = 'cancelado'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('compra.model') or 'New'
        return super(Compra, self).create(vals)
