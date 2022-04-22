
import string
from odoo import api, models, modules, fields


class CrmLead(models.Model):
    _name = "crm.lead" 
    _inherit = 'crm.lead'

    partner_id = fields.Many2one(
        'res.partner', string='Customer khanhhhhhhh', index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    
    email_from = fields.Char(
        'Email *', tracking=40, index=True,
        compute='_compute_email_from', inverse='_inverse_email_from', readonly=False, store=True)
    
    phone = fields.Char(
        'Phone *', tracking=50,
        compute='_compute_phone', inverse='_inverse_phone', readonly=False, store=True)
    
    user_id = fields.Many2one('res.users', string='Salesperson *', index=True, tracking=True, default=lambda self: self.env.user)
    
    team_id = fields.Many2one(
        'crm.team', string='Sales Team *', index=True, tracking=True,
        compute='_compute_team_id', readonly=False, store=True)
    
    date_deadline = fields.Date('Expected Closing *', help="Estimate of the date on which the opportunity will be won.")
    
    # priority = fields.Selection(
    #     crm_stage.AVAILABLE_PRIORITIES, string='Priority *', index=True,
    #     default=crm_stage.AVAILABLE_PRIORITIES[0][0])
    
    partner_name = fields.Char(
        'Company Name *', tracking=20, index=True,
        compute='_compute_partner_name', readonly=False, store=True,
        help='The name of the future partner company that will be created while converting the lead into opportunity')
    
    contact_name = fields.Char(
        'Contact Name *', tracking=30,
        compute='_compute_contact_name', readonly=False, store=True)
    
    mobile = fields.Char('Mobile *', compute='_compute_mobile', readonly=False, store=True)
    
    lang_id = fields.Many2one('res.lang', string='Language *')