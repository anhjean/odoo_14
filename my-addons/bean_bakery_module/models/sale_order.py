from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"
    mobile = fields.Char(related='partner_id.mobile')
    phone = fields.Char(related='partner_id.phone')