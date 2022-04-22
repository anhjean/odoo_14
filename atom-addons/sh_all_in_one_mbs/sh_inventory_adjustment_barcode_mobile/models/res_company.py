# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sh_inventory_adjt_barcode_mobile_type = fields.Selection([
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode'),
        ('sh_qr_code', 'QR code'),
        ('all', 'All')
    ], default='barcode', string='Product Scan Options In Mobile (Stock Adjustment)', translate=True)

    sh_inventory_adjt_bm_is_cont_scan = fields.Boolean(
        string='Continuously Scan? (Stock Adjustment)')

    sh_inventory_adjt_bm_is_notify_on_success = fields.Boolean(
        string='Notification On Product Succeed? (Stock Adjustment)')

    sh_inventory_adjt_bm_is_notify_on_fail = fields.Boolean(
        string='Notification On Product Failed? (Stock Adjustment)')

    sh_inventory_adjt_bm_is_sound_on_success = fields.Boolean(
        string='Play Sound On Product Succeed? (Stock Adjustment)')

    sh_inventory_adjt_bm_is_sound_on_fail = fields.Boolean(
        string='Play Sound On Product Failed? (Stock Adjustment)')
