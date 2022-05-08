from odoo import models, fields, api

class Ward(models.Model):
    _name='res.country.ward'
    _description = 'ward'
    _order = 'name'

    name = fields.Char("Ward name", translate=True)
    code = fields.Char(string="Ward Code")
    slug = fields.Char(string="Ward Code ID")
    district_id = fields.Many2one('res.country.district', string='District')
    