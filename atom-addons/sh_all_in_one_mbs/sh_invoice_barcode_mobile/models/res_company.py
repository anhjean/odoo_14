# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_invoice_barcode_mobile_type = fields.Selection([
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode'),
        ('sh_qr_code', 'QR code'),
        ('all', 'All')
    ], default='barcode', string='Product Scan Options In Mobile (Invoice)', translate=True)

    sh_invoice_bm_is_cont_scan = fields.Boolean(
        string='Continuously Scan? (Invoice)')

    sh_invoice_bm_is_notify_on_success = fields.Boolean(
        string='Notification On Product Succeed? (Invoice)')

    sh_invoice_bm_is_notify_on_fail = fields.Boolean(
        string='Notification On Product Failed? (Invoice)')

    sh_invoice_bm_is_sound_on_success = fields.Boolean(
        string='Play Sound On Product Succeed? (Invoice)')

    sh_invoice_bm_is_sound_on_fail = fields.Boolean(
        string='Play Sound On Product Failed? (Invoice)')
