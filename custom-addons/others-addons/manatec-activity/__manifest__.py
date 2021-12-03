# -*- coding: utf-8 -*-
#   Created by: Alexander Heyber (alexander.heyber@manatec.de)
#   info@manatec.de
#
#   Created 25.02.2019

{
    'name': 'Central Activity View',
    'depends': [
        'mail',
        'calendar',
    ],
    'author': 'manaTec GmbH',
    'website': 'https://www.manatec.de',
    "category": "Base",
    "version": "1.0.0",
    'images': ['static/description/thumbnail.png'],
    'author': 'manaTec GmbH',
    'website': 'https://www.manatec.de',
    'support': 'support@manatec.de',
    'license': 'OPL-1',
    'currency': 'EUR',
    'summary': "A nice overview for all activities",
    'description': "This module adds a nice central overview for all activities in Odoo.",
    'demo': [],
    'data': [
        'security/groups.xml',
        'views/activity_view.xml',
        'views/activity_menuitem.xml',
    ]
}
