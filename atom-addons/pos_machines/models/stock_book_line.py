from odoo import fields, models, api


class StockBookLine(models.Model):
    _name = 'stock.book.line'
    _description = 'Description'

    partner_id = fields.Many2one('res.partner', string='Hồ sơ')
    picking_id = fields.Many2one('stock.picking', string='Phiếu')
