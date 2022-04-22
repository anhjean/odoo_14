# -*- coding: utf-8 -*-

# File: stock_move_line.py	
# Created at 29/11/2021

"""
   Description: 
        -
        -
"""
from odoo import models, fields, api


class StockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'

    has_booked = fields.Boolean(string='Đặt máy làm hồ sơ')

    @api.model
    def name_search(self, name, args, limit, operator):
        if not isinstance(args, list):
            args = []

        args.append(['has_booked', '=', False])

        return super(StockProductionLot, self).name_search(name=name, args=args, limit=limit, operator=operator)
