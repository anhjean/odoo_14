# -*- coding: utf-8 -*-
from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_stock_import(self):
        action = self.env.ref('pways_import_stock_move_line_xls.action_stock_import_wizard').read()[0]
        action.update({'views': [[False, 'form']]})
        return action
