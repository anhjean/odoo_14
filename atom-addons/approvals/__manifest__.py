# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Approvals',
    'version': '14.0.0.1',
    'license': 'AGPL-3',
    'category': 'Human Resources/Approvals',
    'summary': 'Create and validate approvals requests',
    'description': """
        This module manages the Internal approvals workflow
        ======================================

        This module manages approval requests 
        According to the approval type configuration, a request
        creates next activities for the related approvers.
    """,
    'depends': ['mail', 'hr', 'product'],
    'data': [
        'security/approval_security.xml',
        'security/ir.model.access.csv',

        'data/approval_category_data.xml',
        'data/mail_activity_data.xml',

        'views/approval_template.xml',
        'views/approval_category_views.xml',
        'views/approval_product_line_views.xml',
        'views/approval_request_views.xml',
        'views/res_users_views.xml',
    ],
    'demo':[
        'data/approval_demo.xml',
    ],
    'qweb': [
        'static/src/bugfix/bugfix.xml',
        'static/src/components/activity/activity.xml',
        'static/src/components/approval/approval.xml',
        'static/src/xml/*.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    
}
