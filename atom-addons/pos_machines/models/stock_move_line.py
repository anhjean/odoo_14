# -*- coding: utf-8 -*-

# File: sock_move_line.py	
# Created at 29/11/2021

"""
   Description: 
        -
        -
"""
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = 'stock.move.line'

    account = fields.Many2one('account.pos.machines',
                              string='Tài khoản máy')

    is_setup = fields.Boolean(string="Cài máy")

    @api.model
    def create(self, vals):
        pink = self.env['stock.picking'].search_read([('id', '=', vals.get('picking_id'))])

        vals['is_setup'] = False

        if pink and pink[0].get('name'):
            _name = pink[0].get('name').split('/')
            if len(_name) > 2 and _name[1] == 'OUT':
                vals['is_setup'] = True

        row = super(StockMoveLine, self).create(vals)
        return row

    @api.model
    def write(self, vals, *args, **kwargs):
        if vals.get('lot_id'):
            vals['account'] = None
        rows = super(StockMoveLine, self).write(vals)

        return rows

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.account and self.account.lot_id.id != self.lot_id.id:
            self.account = None

    def setting_account(self):
        account = self.account
        if not account:
            partner_id = self.picking_id.partner_id
            account = self.env['account.pos.machines'].create({
                'lot_id': self.lot_id.id,
                'partner_id': partner_id.id,
                'move_line_id': self.id,
                'username': f"{partner_id.id}-{self.lot_id.id}",
                'status': 'active'
            })
            self.write({
                'account': account.id
            })
        view_id = self.env.ref('pos_machines.account_pos_machines_form_view').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Cài đặt máy',
            'res_model': 'account.pos.machines',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': account.id,
            'view_id': view_id,
            'target': 'new',
            'context': {}
        }

    def account_get(self):
        print('account_get', self)
        if self.reference.split('/')[1] == 'OUT':
            return self.account
        return -1

    @api.model
    def _read_group_many2one_lot_id(self, records, domain, order):
        print('_read_group_many2one_lot_id', records, domain, order)
        return records

    def button_booking(self):

        self.lot_id.write({
            'has_booked': True
        })

        return True

    def gen_account(self):
        return True
