from odoo import models, fields

class Suplemento(models.Model):
    _name = "suplemento.model"
    _description = "Gestión de suplementos nutricionales"

    # Campos básicos
    name = fields.Char('Nombre del suplemento', required=True)
    descripcion = fields.Text('Descripción', help='Introduce una descripción detallada del suplemento')
    codigo = fields.Char('Código de producto', required=True)
    fecha_fabricacion = fields.Date('Fecha de fabricación')
    fecha_vencimiento = fields.Date('Fecha de vencimiento')
    precio = fields.Float('Precio', required=True)
    stock = fields.Integer('Stock disponible', required=True)
    tipo = fields.Selection(
        string='Tipo de suplemento',
        selection=[
            ('vitaminas', 'Vitaminas'),
            ('proteinas', 'Proteínas'),
            ('minerales', 'Minerales'),
            ('aminoacidos', 'Aminoácidos'),
            ('otros', 'Otros'),
        ],
        required=True
    )
    peso = fields.Float('Peso (g)', help='Peso en gramos del suplemento')
    marca = fields.Char('Marca del suplemento')
    es_organico = fields.Boolean('¿Es orgánico?')
    es_apto_vegano = fields.Boolean('¿Apto para veganos?')

    # Campos relacionados (por ejemplo, relación con proveedores)
    proveedor_id = fields.Many2one('res.partner', string='Proveedor', help='Proveedor del suplemento')

    imagen = fields.Binary(string='Imagen')
