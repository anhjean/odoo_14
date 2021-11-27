# -*- coding: utf-8 -*-

import logging
from typing import Sequence

from odoo import api, fields, models,_
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

class invoiceQrFields(models.Model):
    _name = 'invoice.qr.fields'
    _order = 'sequence'

    sequence = fields.Integer()
    field_id = fields.Many2one('ir.model.fields',domain=[('model_id.model','=','account.move'),('ttype','not in',['many2many','one2many','binary'])])
    company_id = fields.Many2one('res.company')

class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_qr_type = fields.Selection([('by_url','Invoice Url'),('by_info','Invoice Text Information')],default='by_url',required=True)
    invoice_field_ids = fields.One2many('invoice.qr.fields','company_id',string="Invoice Field's")

    @api.constrains('invoice_qr_type','invoice_field_ids')    
    def check_invoice_field_ids(self):
        if self.invoice_qr_type == 'by_info' and not self.invoice_field_ids:
            raise UserError(_("Please Add Invoice Field's"))