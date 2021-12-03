# -*- coding: utf-8 -*-
{
    'name': 'Import Stock Inventory',
    'version': '14.0.0',
    'summary': 'This app helps to import stock inventory adjustment from xls file',
    'description': """ This app helps to import stock inventory adjustment from xls file """,
    'category' : 'Warehouses',
    'author': 'Preciseways',
    'website': 'http://www.preciseways.com',
    'depends': ['stock'],
    'data': [
            "security/ir.model.access.csv",
            "security/excess_right.xml",
            "views/stock_view.xml",

             ],
    'installable': True,
    'application': True,
    'images':['static/description/banner.png'],
    'license': 'OPL-1',
}
