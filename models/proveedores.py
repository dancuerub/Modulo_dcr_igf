from odoo import models, fields

class Proveedor(models.Model):
    _name = 'proveedor.model'
    _description = 'Gestión de Proveedores'

    name = fields.Char('Nombre de la Empresa', required=True)
    contacto = fields.Char('Persona de Contacto')
    email = fields.Char('Correo Electrónico')
    phone = fields.Char('Teléfono')
    direccion = fields.Char('Dirección')
    ciudad = fields.Char('Ciudad')
    pais = fields.Char('País')
    activo = fields.Boolean('Activo', default=True)

    suplementos_ids = fields.One2many('suplemento.model', 'proveedor_id', string='Suplementos')