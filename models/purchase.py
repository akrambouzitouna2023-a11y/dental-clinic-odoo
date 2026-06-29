from odoo import models, fields, api

class DentalPurchase(models.Model):
    _name = 'dental.purchase'
    _description = 'Dental Purchase'
    _order = 'purchase_date desc, id desc'

    material_name = fields.Char(string='Material Name', required=True)
    supplier = fields.Char(string='Supplier')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price (DZD)', default=0.0)
    purchase_date = fields.Date(string='Purchase Date', default=fields.Date.today)
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.quantity * rec.unit_price
