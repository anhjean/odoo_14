# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    district_id = fields.Many2one( comodel_name='res.country.district',string='District',domain="[('state_id', '=', state_id)]")
    ward_id = fields.Many2one(comodel_name='res.country.ward',string='Ward',domain="[('district_id', '=', district_id)]")





