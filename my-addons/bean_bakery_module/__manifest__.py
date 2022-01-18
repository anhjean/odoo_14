# -*- coding: utf-8 -*-
{
    'name': "Bean Bakery Modules",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Bean Bakery",
    'website': "http://www.beanbakery.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contact',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product.xml',
        # 'views/templates.xml',
        'views/res_partner.xml',
        #'views/library_book.xml',
        'security/groups.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    # securities csv for Library
    #acl_book,library.book default,model_library_book,,1,1,1,1
    #acl_book_category,library.book.category,model_library_book_category,,1,1,1,1
    #acl_book_library,library.book_librarian,model_library_book,group_librarian,1,1,1,1
}
