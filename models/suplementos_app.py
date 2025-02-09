from odoo import models, fields
from odoo.exceptions import UserError

class Suplemento(models.Model):
    _name = "suplemento.model"
    _description = "Gestión de suplementos nutricionales"

    # Campos básicos
    name = fields.Char('Nombre del suplemento', required=True)
    descripcion = fields.Text('Descripción', help='Introduce una descripción detallada del suplemento')
    codigo = fields.Char('Código de producto', required=True)
    fecha_fabricacion = fields.Date('Fecha de fabricación')
    fecha_vencimiento = fields.Date('Fecha de vencimiento')
    precio_venta = fields.Float('Precio Venta', required=True)
    precio_compra = fields.Float('Precio Compra', required=True)
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

    active = fields.Boolean(default=True)

    # Campos relacionados (por ejemplo, relación con proveedores)
    proveedor_id = fields.Many2one('proveedor.model', string='Proveedor', required=True, help='Proveedor del suplemento')

    imagen = fields.Binary(string='Imagen')

    # Nuevos campos nutricionales
    dosis_recomendada = fields.Char('Dosis Recomendada', help='Cantidad recomendada por día')
    valor_energetico = fields.Float('Valor Energético (kcal)', help='Cantidad de energía en kilocalorías')
    grasas = fields.Float('Grasas (g)', help='Cantidad de grasas en gramos')
    hidratos_carbono = fields.Float('Hidratos de Carbono (g)', help='Cantidad de carbohidratos en gramos')
    proteinas = fields.Float('Proteínas (g)', help='Cantidad de proteínas en gramos')
    sal = fields.Float('Sal (g)', help='Cantidad de sal en gramos')

    # Selección de vitaminas (muchos a muchos)
    vitaminas = fields.Many2many(
        'vitamina.model',
        'suplemento_vitamina_rel',
        'suplemento_id',
        'vitamina_id',
        string='Vitaminas Contenidas'
    )

    def unlink(self):
        for record in self:
            if record.active:
                # Aquí estamos "eliminando" pero en realidad archivando
                record.write({'active': False})

                # Mostrar mensaje emergente informando que el producto ha sido archivado
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Producto Archivado',
                        'message': 'El producto no ha sido eliminado, ha sido archivado correctamente.',
                        'type': 'success',  # Tipo de notificación
                        'sticky': False,  # Si es True, la notificación no desaparecerá
                    }
                }

            else:
                # Si el producto ya está archivado, lanzamos un error
                raise UserError('Este producto ya está archivado.')