# Part of Softhealer Technologies.
{
    "name": "POS Mobile Barcode Scanner | POS Mobile QRCode Scanner | Point Of Sale Mobile Barcode Scanner | Point Of Sale Mobile QRCode Scanner",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "14.0.2",

    "category": "Point Of Sale",
    
    "license": "OPL-1",

    "summary": "Scan POS Product Mobile Barcode Module, Scan POS Product Mobile QRCode, Point Of Sale Mobile QRCode Scanner App, Point Of Sale Product QR Scanner Odoo",

    "description": """Do you want to scan POS(Point Of Sale) products by Barcode or QRCode on your mobile? Do your time-wasting in POS(Point Of Sale) operations by manual product selection? So here are the solutions these modules useful do quick operations of POS mobile Barcode or QRCode scanner. You no need to select the product and do one by one. scan it and you do! So be very quick in all operations of odoo in mobile and cheers!""",

    "depends": ['point_of_sale', 'sh_product_qrcode_generator'],

    "data": [
        "views/views.xml",
        "static/src/xml/templates.xml"
    ],
    "qweb": ["static/src/xml/*.xml", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/yTQ4GeVs6Ww",
    "price": 60,
    "currency": "EUR"
}
