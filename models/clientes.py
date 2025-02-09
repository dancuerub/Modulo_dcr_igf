from odoo import models, fields
from odoo.exceptions import UserError

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

    active = fields.Boolean(default=True)

    def unlink(self):
        for record in self:
            if record.active:
                # Aquí estamos "eliminando" pero en realidad archivando
                record.write({'active': False})

                # Mostrar mensaje emergente informando que el cliente ha sido archivado
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Cliente Archivado',
                        'message': 'El cliente no ha sido eliminado, ha sido archivado correctamente.',
                        'type': 'success',  # Tipo de notificación
                        'sticky': False,  # Si es True, la notificación no desaparecerá
                    }
                }

            else:
                # Si el cliente ya está archivado, lanzamos un error
                raise UserError('Este cliente ya está archivado.')