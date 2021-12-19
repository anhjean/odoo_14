# -*- coding: utf-8 -*-

from odoo import models, api

try:
    import requests
    import json
except ImportError:
    pass


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('vat')
    def get_company_info_from_vat(self):
        if self.vat:
            url = 'https://thongtindoanhnghiep.co/api/company/' + self.vat
            res = requests.get(url, verify=True, )
            data = None
            if res.status_code == 200:
                data = json.loads(res.text)
            if data and 'ID' in data and data['ID'] is not None:
                self.name = data['Title']
                self.street = data['DiaChiCongTy']
                self.city = data['TinhThanhTitle']
                results = self.env['res.country.state'].search([('country_id', '=', 241), \
                                                                ('name', '=', self.city)])
                self.state_id = results.id
                self.phone = data['NoiDangKyQuanLy_DienThoai']
                if 0 != data['ID']:
                    self.country_id=241
                else:
                    self.country_id=0
