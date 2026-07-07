from odoo import models, fields

class DentalTooth(models.Model):
    _name = 'dental.tooth'
    _description = 'Dental Tooth'
    _order = 'id'

    name = fields.Char(string='Tooth', required=True)
    number = fields.Integer(string='Number', required=True)
