from odoo import fields, models, api


class PosFunctions(models.Model):
    _name = 'pos.functions'
    _description = 'Description'
    _rec_name = 'name'

    name = fields.Selection(selection=[('pre_auth', 'Pre Auth'), ('tip', 'Tip')], default='pre_auth')
    disable = fields.Boolean(string='Khóa', default=True)
    pos_account_id = fields.Many2one('account.pos.machines', string='Tài khoản', readonly=True, auto_join=True)
    bank_id = fields.Many2one('res.bank', string='Ngân hàng')
