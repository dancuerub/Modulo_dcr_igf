from odoo import models, fields

class Vitamina(models.Model):
    _name = "vitamina.model"
    _description = "Vitaminas Disponibles"

    name = fields.Char('Nombre de la Vitamina', required=True)