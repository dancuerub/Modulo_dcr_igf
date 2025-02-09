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

    active = fields.Boolean(default=True)

    def unlink(self):
        for record in self:
            if record.active:
                # Aquí estamos "eliminando" pero en realidad archivando
                record.write({'active': False})

                # Mostrar mensaje emergente informando que el proveeedor ha sido archivado
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Cliente Archivado',
                        'message': 'El proveedor no ha sido eliminado, ha sido archivado correctamente.',
                        'type': 'success',  # Tipo de notificación
                        'sticky': False,  # Si es True, la notificación no desaparecerá
                    }
                }

            else:
                # Si el proveedor ya está archivado, lanzamos un error
                raise UserError('Este proveedor ya está archivado.')