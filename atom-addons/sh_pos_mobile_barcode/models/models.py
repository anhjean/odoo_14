# Copyright (C) Softhealer Technologies.
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sh_pos_barcode_mobile_type = fields.Selection([
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode'),
        ('sh_qr_code', 'QR code'),
        ('all', 'All')
    ], string='Product Scan Options In Mobile (Point of Sale)', readonly=False, default='barcode')

    sh_pos_bm_is_cont_scan = fields.Boolean(
        'Continuously Scan?', readonly=False)

    sh_pos_bm_is_notify_on_success = fields.Boolean(
        string='Notification On Product Succeed?', readonly=False)

    sh_pos_bm_is_notify_on_fail = fields.Boolean(
        string='Notification On Product Failed?', readonly=False)

    sh_pos_bm_is_sound_on_success = fields.Boolean(
        'Play Sound On Product Succeed?', readonly=False)

    sh_pos_bm_is_sound_on_fail = fields.Boolean(
        'Play Sound On Product Failed?', readonly=False)
