# -*- coding: utf-8 -*-
{
    "name": "Dynamic Add to Cart",
    "summary": """
    Add to Cart button adds items to the cart without refreshing/redirecting website
    """,
    "description": """
        Add to Cart button adds items to the cart without refreshing/redirecting website
    """,
    "author": "Peter M. Fam",
    "website": "https://petermfam.me",
    "license": "GPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Website",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "website_sale", "website"],
    # always loaded
    "data": [
        "views/assets.xml",
    ],
    "images": ["images/main_screenshot.gif"],
}
