from odoo import models, fields, api

class Ward(models.Model):
    _name='res.country.ward'
    _description = 'ward'
    _order = 'name'

    # ward_id = fields.One2many('res.partner',string='Ward')
    name = fields.Char("Ward name", translate=True)
    district_id = fields.Many2one('res.country.district', string='District')
    #ward_id = fields.Many2one('res.ward.district', 'Ward')
        # 'res.ward.district', 'Ward', domain="[('district_id', '=', district_id)]")