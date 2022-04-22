import hashlib
import hmac
import json

import requests

from odoo import fields, models, api, tools


def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()


class AccountPosMachines(models.Model):
    _name = 'account.pos.machines'
    _rec_name = 'username'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    _description = 'Pos machines'

    move_line_id = fields.Many2one(
        'stock.move.line')

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number', readonly=True)

    username = fields.Char(
        string="Tài khoản",
        readonly=True
    )

    partner_id = fields.Many2one('res.partner', string="Merchant")

    states = fields.Selection(selection='get_states_options', string='Trạng thái máy', tracking=True)

    ref_codes = fields.One2many('ref.code', 'account_id', string="Mã ref")

    disable_functions = fields.One2many('pos.functions', 'pos_account_id')
    stock_out_picking_id = fields.Many2one('stock.picking')
    status = fields.Char(default='active')

    @api.model
    def get_states_options(self):
        options = self.env['master.data'].search_read(
            [('field', '=', 'states'), ('model', '=', 'account.pos.machines')])
        return [(x.get('value'), x.get('name')) for x in options]

    note = fields.Text(string='Ghi chú')

    def send_backend(self):
        self.ensure_one()
        secret_key = tools.config['mms_secret_key']  # 'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
        api_domain = tools.config['api_domain']
        api_key = tools.config['mms_api_key']
        supporter_id = self.partner_id.supporter_id
        contact_seller = {
            'phone': '',
            'email': '',
            'name': '',
            'company': self.partner_id.company_id.name,
            'mms_user_id': 0
        }

        if supporter_id:
            contact_seller['phone'] = supporter_id.mobile_phone or ''
            contact_seller['email'] = supporter_id.work_email or ''
            contact_seller['name'] = supporter_id.name or ''
            contact_seller['mms_user_id'] = supporter_id.id
        company_code = self.partner_id.parent_id.company_id.company_code if self.partner_id.parent_id else self.partner_id.company_id.company_code
        value = {
            "serial_number": self.lot_id.name,
            "ref_codes": [x.ref_no for x in self.ref_codes],
            "disable_functions": [x.name for x in self.disable_functions],
            "odoo_contact_id": str(self.partner_id.id),
            "username": self.username,
            'password': '000000',
            "pos_address": {
                "city": self.partner_id.state_id.name or '',
                "district": self.partner_id.city or '',
                "ward": self.partner_id.street2 or '',
                "detail": self.partner_id.street or ''
            },
            "merchant": {
                "name": self.partner_id.name,
                "address": {
                    "city": self.partner_id.state_id.name or '',
                    "district": self.partner_id.city or '',
                    "ward": self.partner_id.street2 or '',
                    "detail": self.partner_id.street or ''
                },
                'company_code': company_code or 'paydi'
            },
            'contact_seller': contact_seller
        }
        # print('send_backend', value)

        gen_data = sorted(value.items())
        string_data = json.dumps(gen_data)
        hash_string = sha512(string_data, secret_key)
        headers = {
            'Content-Type': 'application/json'
        }
        url = f"{api_domain}/v1/auth/iapi/pos/gen_account?api_key={api_key}"

        payload = json.dumps({
            **value,
            "code": hash_string
        })
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        if not response.status_code == 200:
            raise Exception

        return True

    def blocked_machine(self):
        # self.ensure_one()
        secret_key = tools.config['mms_secret_key']  # 'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
        api_domain = tools.config['api_domain']
        api_key = tools.config['mms_api_key']

        value = {
            "serial_number": self.lot_id.name,
            "username": self.username,
            "status": "blocked"
        }
        # print('send_backend', value)
        gen_data = sorted(value.items())
        string_data = json.dumps(gen_data)
        hash_string = sha512(string_data, secret_key)
        headers = {
            'Content-Type': 'application/json'
        }
        url = f"{api_domain}/v1/auth/iapi/pos/change_status?api_key={api_key}"

        payload = json.dumps({
            **value,
            "code": hash_string
        })
        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)

        if not response.status_code == 200:
            raise Exception
        self.write({
            'status': 'blocked'
        })
        return True

    def active_machine(self):
        # self.ensure_one()
        secret_key = tools.config['mms_secret_key']  # 'x4nz(!jh6c+jvo5aanhy*=cx(8!uh85e&ocf3*py%*vw#$^g6c'
        api_domain = tools.config['api_domain']
        api_key = tools.config['mms_api_key']

        value = {
            "serial_number": self.lot_id.name,
            "username": self.username,
            "status": "active"
        }
        # print('send_backend', value)
        gen_data = sorted(value.items())
        string_data = json.dumps(gen_data)
        hash_string = sha512(string_data, secret_key)
        headers = {
            'Content-Type': 'application/json'
        }
        url = f"{api_domain}/v1/auth/iapi/pos/change_status?api_key={api_key}"

        payload = json.dumps({
            **value,
            "code": hash_string
        })
        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)

        if not response.status_code == 200:
            raise Exception
        self.write({
            'status': 'active'
        })
        return True

    @api.model
    def create(self, vals):
        pos_account = super().create(vals)
        return pos_account

    @api.model_create_multi
    def create(self, vals_list):
        return super(AccountPosMachines, self).create(vals_list=vals_list)
