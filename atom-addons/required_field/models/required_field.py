import string
from typing_extensions import Required
from odoo import api, models, modules, fields


class RequiredField(models.Model):
    _name = "crm.lead" 
    _inherit = 'crm.lead'

    street = fields.Char('Street', Required=True , compute='_compute_partner_address_values', readonly=False, store=True)