# -*- coding: utf-8 -*-

from typing_extensions import Self
from pandas import concat
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    city_id = fields.Many2one( comodel_name='res.country.city',string='City',domain="[('state_id', '=', state_id)]")
    district_id = fields.Many2one( comodel_name='res.country.district',string='District',domain="[('city_id', '=', city_id)]")
    ward_id = fields.Many2one(comodel_name='res.country.ward',string='Ward',domain="[('district_id', '=', district_id)]")
    city =fields.Char(related='city_id.name', store=True)
    
    def _makeaddress(self,ward_name = "", district_name = ""):
        return (ward_name + ", " + district_name)
    
    @api.onchange('district_id')
    def _district_onchange(self):
        print(self.ward_id.name)
        if (self.ward_id.name):
            self.street2 = self._makeaddress(self.ward_id.name , self.district_id.name)
        else:
            self.street2 = self._makeaddress(district_name = self.district_id.name)
    
    @api.onchange('ward_id')
    def _ward_onchange(self):
        if (self.district_id.name):
            self.street2 = self._makeaddress(self.ward_id.name , self.district_id.name)
        else:
            self.street2 = self._makeaddress(ward_name = self.district_id.name)
        
    



