from odoo import models, fields, api
from datetime import date

class DentalPatient(models.Model):
    _name = 'dental.patient'
    _description = 'Dental Patient'
    _order = 'create_date desc'

    name = fields.Char(string='Patient Name', compute='_compute_name', store=True)
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    age = fields.Integer(string='Age', required=True)
    phone = fields.Char(string='Phone Number', required=True)
    
    treatment_category = fields.Selection([
        ('fixe', 'Prothèse Fixe'),
        ('amovible', 'Prothèse Amovible'),
    ], string='Treatment Category', required=True)
    
    fixe_type = fields.Selection([
        ('couronne', 'Couronne'),
        ('bridge', 'Bridge'),
        ('inlay', 'Inlay/Onlay'),
    ], string='Fixe Type')
    
    amovible_type = fields.Selection([
        ('totale', 'Prothèse Totale'),
        ('partielle', 'Prothèse Partielle'),
    ], string='Amovible Type')
    
    partielle_subtype = fields.Selection([
        ('resine', 'Résine'),
        ('metal', 'Métal'),
        ('flexible', 'Flexible'),
    ], string='Partielle Subtype')
    
    simple_treatment = fields.Selection([
        ('extraction', 'Extraction'),
        ('canal', 'Traitement Canalaire'),
        ('obturation', 'Obturation'),
        ('composite', 'Restauration Composite'),
        ('detartrage', 'Detartrage'),
        ('consultation', 'Consultation'),
    ], string='Simple Treatment')
    
    cost = fields.Float(string='Total Price (DZD)', required=True, default=0.0)
    amount_paid = fields.Float(string='Amount Paid (DZD)', default=0.0)
    remaining_amount = fields.Float(string='Remaining Amount', compute='_compute_remaining', store=True)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Status', default='new')
    
    medical_history = fields.Text(string='Medical History', help='Patient history and allergies')

    tooth_ids = fields.Many2many("dental.tooth", string="Selected Teeth")
    
    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for patient in self:
            patient.name = f"{patient.first_name or ''} {patient.last_name or ''}".strip()
    
    @api.depends('cost', 'amount_paid')
    def _compute_remaining(self):
        for patient in self:
            patient.remaining_amount = patient.cost - patient.amount_paid
    
    def action_start_treatment(self):
        self.write({'state': 'in_progress'})
    
    def action_complete_treatment(self):
        self.write({'state': 'done'})
