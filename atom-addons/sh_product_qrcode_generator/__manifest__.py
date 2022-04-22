# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

{
    "name": "Product QR Code Generator",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "version": "14.0.8",

    "category": "Extra Tools",
    
    "license": "OPL-1",

    "summary": " Default Make QR Module,New Product QR Generate App,Existing Product QR Generate Application, Existing Multi Product QR Create, Custom Product QR Generator,Product QRCode Generator,QRCode Product Odoo",

    "description": """This module automatically generates QR Code for the Product. It allows for generating QR Code for existing products. Generate QR Code on new product creation. This module helps to set up a unique QR Code for products. This module provides functionality to generate product QR Code If already exists.

 Automatic Generate Product QR Odoo
 By Default Make QR Module, Auto Generate New Product QR, Automatic Generate Existing Product QR, Auto Create Existing Multi Product QR, Custom Product QR Generator Odoo.""",

    "depends": [
            "product",
            "base_setup"
        ],

    "images": ["static/description/background.png", ],

    "data": [

            "data/ir_sequence_data.xml",
            "security/product_qr_code.xml",
            "security/ir.model.access.csv",
            "views/res_config_settings.xml",
            "views/product_view.xml",
            "wizard/qr_generator.xml",

    ],

    "external_dependencies": {
        "python": ["qrcode"],
    },

    "installable": True,
    "auto_install": False,
    "application": True,
    "live_test_url": "https://youtu.be/MnVaXV_GHbk",
    "price": 12,
    "currency": "EUR",   
}
