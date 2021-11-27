{
    'name': "POS Default Customer",
    'version' : '14.1.1.1',
    'summary': 'Using this apps you can select default cusotmer in POS.',
    'category': 'Point of Sale',
    'description': """ Using this apps you can select default cusotmer in POS.""",
    "price": 0,
    'currency': 'EUR',
    "author" : "odoobridge",
     "email": 'odoobridge@gmail.com',
    'sequence': 1,
    'license': 'OPL-1',
    "depends" : ['point_of_sale'],
    'data': [
        'views/point_of_sale.xml',
        'views/pos_config_view.xml',
    ],
    "external_dependencies": {
        "python": [],
        "bin": []
    },     
    'images': [],
    'qweb': [],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}


