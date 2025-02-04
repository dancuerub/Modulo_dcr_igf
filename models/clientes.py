from odoo import models, fields

class Cliente(models.Model):
    _name = 'cliente.model'
    _description = 'Gestión de Clientes'

    name = fields.Char('Nombre Completo', required=True)
    email = fields.Char('Correo Electrónico')
    phone = fields.Char('Teléfono')
    direccion = fields.Char('Dirección')
    ciudad = fields.Char('Ciudad')
    pais = fields.Char('País')
    activo = fields.Boolean('Activo', default=True)