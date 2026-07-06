from odoo import models, fields, api

class DentalPatient(models.Model):
    _name = 'dental.patient'
    _description = 'Dental Patient'
    _order = 'date desc, id desc'

    # === Patient Info ===
    name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    age = fields.Integer(string='Age')
    phone = fields.Char(string='Phone Number')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    email = fields.Char(string='Email')
    medical_history = fields.Text(string='Medical History', help='Patient history and allergies')

    # === Prothèse Fixe ===
    fixe_type = fields.Selection([
        ('ceramo_metal', 'Céramo-métallique'),
        ('zirone', 'Zirone'),
        ('ceramo_ceramide', 'Céramo-céramide'),
        ('emax', 'E-Max'),
        ('resine', 'Résine'),
    ], string='Prothèse Fixe Type')

    # === Prothèse Amovible ===
    amovible_type = fields.Selection([
        ('totale', 'Totale'),
        ('partielle', 'Partielle'),
    ], string='Prothèse Amovible Type')

    # === Sous-types Partielle ===
    partielle_subtype = fields.Selection([
        ('resine_blanche', 'Résine blanche'),
        ('resine_simple', 'Résine simple'),
        ('resine_flexible', 'Résine flexible'),
    ], string='Partielle Subtype')

    # === Main Treatment Category ===
    treatment_category = fields.Selection([
        ('fixe', 'Prothèse Fixe'),
        ('amovible', 'Prothèse Amovible'),
    ], string='Treatment Category', required=True)

    simple_treatment = fields.Selection([
        ('extraction', 'Extraction'),
        ('canal', 'Traitement Canalaire'),
        ('obturation', 'Obturation'),
        ('composite', 'Restauration Composite'),
        ('detartrage', 'Detartrage'),
        ('consultation', 'Consultation'),
    ], string='Simple Treatment')

    # === Cost & Payment ===
    cost = fields.Float(string='Cost (DZD)')
    total_price = fields.Float(string='Total Price (DZD)', default=0.0)
    amount_paid = fields.Float(string='Amount Paid (DZD)', default=0.0)
    remaining_amount = fields.Float(string='Remaining (DZD)', compute='_compute_remaining', store=True)
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ], string='Payment Status', compute='_compute_payment_status', store=True)

    # === State & Dates ===
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], default='new', string='Status')
    date = fields.Date(string='Date', default=fields.Date.today)
    registration_date = fields.Date(string='Registration Date', default=fields.Date.today)

    # === Active (for archive feature) ===
    active = fields.Boolean(string='Active', default=True)

    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.name or ''} {rec.last_name or ''}".strip()

    @api.depends('total_price', 'amount_paid')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining_amount = rec.total_price - rec.amount_paid

    @api.depends('total_price', 'amount_paid')
    def _compute_payment_status(self):
        for rec in self:
            if rec.amount_paid >= rec.total_price and rec.total_price > 0:
                rec.payment_status = 'paid'
            elif rec.amount_paid > 0:
                rec.payment_status = 'partial'
            else:
                rec.payment_status = 'unpaid'

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})
