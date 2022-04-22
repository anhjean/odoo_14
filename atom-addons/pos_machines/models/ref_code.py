from odoo import fields, models, api


class RefCode(models.Model):
    _name = 'ref.code'
    _description = 'Description'

    account_id = fields.Many2one('account.pos.machines', string='Tài khoản')
    bank_id = fields.Many2one('res.bank', string='Ngân hàng')
    ref_no = fields.Char(string='Mã ref code')
