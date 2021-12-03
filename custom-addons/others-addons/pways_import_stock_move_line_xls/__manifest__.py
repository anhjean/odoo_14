# -*- coding: utf-8 -*-
{
    "name": "Import Stock Move Line",
    'summary': 'Import Stock move from xls file',
    'description': """Import stock move from xls file """,
    "version":"14.0.0",
    "category": "Stock",
    'author': 'Preciseways',
    'website': 'http://www.preciseways.com',
    "depends": ['stock'],
    "data": [
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'wizard/stock_import_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'images':['static/description/banner.png'],
    'license': 'OPL-1',
}