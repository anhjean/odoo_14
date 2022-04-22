
import string
from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = "crm.lead" 
    _inherit = 'crm.lead'

    industry = fields.Char('industry', compute='_compute_partner_address_values', readonly=False, store=True)