# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Approvals - Purchase - Stock',
    'version': '14.0.0.1',
    'license': 'AGPL-3',
    'category': 'Human Resources/Approvals',
    'description': """ Technical module to link Approvals, Purchase and Inventory together. """,
    'depends': ['approvals_purchase', 'purchase_stock'],
    'data': [
        'views/approval_product_line_views.xml',
        'views/approval_request_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': True,
}
