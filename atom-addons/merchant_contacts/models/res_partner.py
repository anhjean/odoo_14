# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import string
from odoo import api, models, modules, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    company_vn_name = fields.Char(string='Tên đăng ký(VN)')
    company_en_name = fields.Char(string='Tên đăng ký(EN)')

    obj_type = fields.Selection(selection=[("merchant","Hồ sơ merchant")], string="Loại liên hệ")
    obj_type1 = fields.Many2one(comodel_name="merchant.type",string="Loại Merchant")
    @api.model
    def get_obj_type_options(self):
        options = self.env['master.data'].search_read([('field', '=', 'obj_type'), ('model', '=', 'res.partner')])
        return [(x.get('value'), x.get('name')) for x in options]

    registration_number = fields.Char(string="Số đăng ký kinh doanh")

    # mid = fields.One2many('mms.mid', 'partner_id',  string='Mã mid'2)
    service_ids = fields.One2many('merchant.service', 'partner_id', string="Dịch vụ khác")

    def _get_city_code(self):
        for record in self:
            if record.city:
                record.city_code = self.env['vn.location'].search([('code', '=', record.city_code)], limit=1)

    def _set_city_code(self):
        for record in self:
            if record.city_code:
                record.city = record.city_code.code

    city_id = fields.Many2one('vn.location', string="Tỉnh/TP", domain=[('parent_id', '=', False)])

    district_id = fields.Many2one('vn.location', string="Quận/Huyện")

    ward_id = fields.Many2one('vn.location', string="Phường/xã")

    @api.onchange('city_id')
    def onchange_city_id(self):
        if self.city_id and self.district_id and self.city_id.id != self.district_id.parent_id.id:
            self.district_id = None
            self.ward_id = None

    @api.onchange('district_id')
    def onchange_district_id(self):
        if self.district_id and self.ward_id and self.district_id.id != self.ward_id.parent_id.id:
            self.ward_id = None

    # supporter_id = fields.Many2one('hr.employee',
    #                                check_company=True,
    #                                string="Nhân viên kinh doanh"
    #                                )
    # supporter_department_id = fields.Many2one('hr.department',
    #                                           string="Đội ngũ bán hàng",
    #                                           related='supporter_id.department_id')
    
    support_employee_team = fields.Many2one('crm.team',
                                                string="Đội ngũ chăm sóc")
    
    supporter_employee_id = fields.Many2one('res.users',
                                              string="Nhân viên chăm sóc khách hàng",
                                              domain="[('sale_team_id', '=', support_employee_team)]"
                                              )
    
    profile_status = fields.Selection([ ('1', 'Đang đàm phán'),('2', 'Đã ký hợp đồng'),('3','Đã cấp máy')],'Trạng thái hồ sơ', default='1')


