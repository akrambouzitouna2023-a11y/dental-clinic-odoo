from odoo import models, fields, api

class ProfitReport(models.TransientModel):
    _name = 'dental.profit.report'
    _description = 'Profit Report Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    total_revenue = fields.Float(string='Total Revenue', readonly=True)
    total_cost = fields.Float(string='Total Cost', readonly=True)
    net_profit = fields.Float(string='Net Profit', readonly=True)

    def action_calculate(self):
        for rec in self:
            # Revenue from patients (amount paid)
            patients = self.env['dental.patient'].search([
                ('date', '>=', rec.start_date),
                ('date', '<=', rec.end_date),
            ])
            rec.total_revenue = sum(patients.mapped('amount_paid'))

            # Cost from purchases
            purchases = self.env['dental.purchase'].search([
                ('purchase_date', '>=', rec.start_date),
                ('purchase_date', '<=', rec.end_date),
            ])
            rec.total_cost = sum(purchases.mapped('total_cost'))

            # Net profit
            rec.net_profit = rec.total_revenue - rec.total_cost
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dental.profit.report',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
