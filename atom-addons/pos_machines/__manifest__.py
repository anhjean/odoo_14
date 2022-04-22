{
    'name': 'Account POS Machines',
    'version': '0.1',
    'summary': 'Summery',
    'description': 'Description',
    'category': 'Sales',
    'depends': ['mail', 'master_data', 'stock'],
    'data': [
        'views/account_pos_machines_view.xml',
        'views/stock_booking_picking_view.xml',
        'security/ir.model.access.csv',
        'views/stock.picking.from.booking.xml',
        'views/pos.functions.view.xml',
        'views/res_partner_fee_view.xml',
        'views/res_partner_views.xml',
        'views/stock_move_line.xml',
        'views/stock.book.line.views.xml',
        'views/stock_picking.xml',
        'views/ref.code.views.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True
}
