
import string
from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = 'merchant.type'
    
    type=fields.Char(string="Loại Merhant",)