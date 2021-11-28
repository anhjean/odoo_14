{
    "name" : "POS Direct Login (Community & Enterprise)",
    "author" : "odoobridge",
    "email": 'odoobridge@gmail.com',
    "category": "Point of Sale",
    "summary": "Using this module you can direct login in to POS without using Backend.",
    "description": """
    Using this module you can direct login in to POS without using Backend
    """,    
    'version': '14.1.1.1',
    "sequence": 1,     
    "license": 'OPL-1',
    "depends" : ['base','point_of_sale'],
    "data" : ['views/res_users_view.xml',
            ], 
    "live_test_url" : "https://youtu.be/hIc85x904dk",
    'qweb': [
        ],
    "images": ['static/description/main_screenshot.png'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    "price": 0,
    "currency": "EUR"   
}


