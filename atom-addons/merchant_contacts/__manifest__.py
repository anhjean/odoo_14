# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Quản lý merchant',
    'category': 'Sales',
    'summary': '',
    'depends': ['base', 'mail', 'account', 'vn_administrative','hr','master_data','crm'],
    'data': [
        'views/res_partner_views.xml',
        'views/merchant_service.xml',
        'security/ir.model.access.csv'
    ],
    'application': True
}
