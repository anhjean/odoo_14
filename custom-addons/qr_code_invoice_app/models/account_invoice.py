# -*- coding: utf-8 -*-
from odoo import models, fields, api ,_
from odoo.http import request
from .qr_generator import generateQrCode
from odoo.tools import html2plaintext


class QRCodeInvoice(models.Model):
    _inherit = 'account.move'

    qr_image = fields.Binary("QR Code", compute='_generate_qr_code')
    partner_vat = fields.Char(string='Partner Tax ID',related="partner_id.vat",store=True, index=True, help="The Parnter Tax Identification Number.")
    company_vat = fields.Char(string='Company Tax ID',related="partner_id.vat",store=True, index=True, help="Your Company Tax Identification Number.")

    def _generate_qr_code(self):
        qr_info = ''
        if self.env.user.company_id.invoice_qr_type != 'by_info':
            qr_info = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            qr_info += self.get_portal_url()
        else:   
            if self.env.user.company_id.invoice_field_ids:
                result = self.search_read([('id', 'in', self.ids)],
                self.env.user.company_id.invoice_field_ids.mapped('field_id.name'))
                dict_result = {}   
                for ffild in self.env.user.company_id.invoice_field_ids.mapped('field_id'):
                    if ffild.ttype == 'many2one':
                        dict_result[ffild.field_description] = self[ffild.name].display_name
                    else:
                        dict_result[ffild.field_description] = self[ffild.name]
                for key,value in dict_result.items():
                    if str(key).__contains__('Partner') or str(key).__contains__(_('Partner')):
                        if self.move_type in ['out_invoice','out_refund']:
                            key = str(key).replace(_('Partner'),_('Customer'))    
                        elif self.move_type in ['in_invoice','in_refund']:
                            key = str(key).replace(_('Partner'),_('Vendor'))   
                    qr_info += f"{key} : {value} <br/>" 
                qr_info = html2plaintext(qr_info)                                                                                                                                 
        self.qr_image = generateQrCode.generate_qr_code(qr_info)
