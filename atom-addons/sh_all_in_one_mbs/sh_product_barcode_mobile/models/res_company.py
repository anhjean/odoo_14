# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_product_barcode_mobile_type = fields.Selection([
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode'),
        ('sh_qr_code', 'QR code'),
        ('all', 'All')
    ], default='barcode', string='Product Scan Options In Mobile (Product)', translate=True)

    sh_product_bm_is_cont_scan = fields.Boolean(
        string='Continuously Scan? (Product)')

    sh_product_bm_is_notify_on_success = fields.Boolean(
        string='Notification On Product Succeed? (Product)')

    sh_product_bm_is_notify_on_fail = fields.Boolean(
        string='Notification On Product Failed? (Product)')

    sh_product_bm_is_sound_on_success = fields.Boolean(
        string='Play Sound On Product Succeed? (Product)')

    sh_product_bm_is_sound_on_fail = fields.Boolean(
        string='Play Sound On Product Failed? (Product)')

    sh_product_bm_is_default_code = fields.Boolean(
        string='Show Internal Reference? (Product)')

    sh_product_bm_is_lst_price = fields.Boolean(
        string='Show Sale Price? (Product)')

    sh_product_bm_is_qty_available = fields.Boolean(
        string='Show Quantity On Hand? (Product)')

    sh_product_bm_is_virtual_available = fields.Boolean(
        string='Show Forecast Quantity? (Product)')
