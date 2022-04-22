# -*- coding: utf-8 -*-

# File: m_service.py	
# Created at 23/11/2021
from odoo import api, models, modules, fields


class MService(models.Model):
    _name = 'merchant.service'

    name = fields.Selection(selection='get_name_options', string="Dịch vụ")

    @api.model
    def get_name_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'name'), ('model', '=', 'merchant.service')])
        return [(x.get('value'), x.get('name')) for x in options]

    has_used = fields.Boolean(string="Có dùng")
    note = fields.Char(string="Ghi chú")

    partner_id = fields.Many2one('res.partner', string='Hồ sơ', domain=[('obj_type', '=', 'merchant')])
