# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_product_barcode_mobile_type = fields.Selection(
        related='company_id.sh_product_barcode_mobile_type', string='Product Scan Options In Mobile (Product)', translate=True, readonly=False)

    sh_product_bm_is_cont_scan = fields.Boolean(
        related='company_id.sh_product_bm_is_cont_scan', string='Continuously Scan? (Product)', readonly=False)

    sh_product_bm_is_notify_on_success = fields.Boolean(
        related='company_id.sh_product_bm_is_notify_on_success', string='Notification On Product Succeed? (Product)', readonly=False)

    sh_product_bm_is_notify_on_fail = fields.Boolean(
        related='company_id.sh_product_bm_is_notify_on_fail', string='Notification On Product Failed? (Product)', readonly=False)

    sh_product_bm_is_sound_on_success = fields.Boolean(
        related='company_id.sh_product_bm_is_sound_on_success', string='Play Sound On Product Succeed? (Product)', readonly=False)

    sh_product_bm_is_sound_on_fail = fields.Boolean(
        related='company_id.sh_product_bm_is_sound_on_fail', string='Play Sound On Product Failed? (Product)', readonly=False)

    sh_product_bm_is_default_code = fields.Boolean(
        related='company_id.sh_product_bm_is_default_code', string='Show Internal Reference? (Product)', readonly=False)

    sh_product_bm_is_lst_price = fields.Boolean(
        related='company_id.sh_product_bm_is_lst_price', string='Show Sale Price? (Product)', readonly=False)

    sh_product_bm_is_qty_available = fields.Boolean(
        related='company_id.sh_product_bm_is_qty_available', string='Show Quantity On Hand? (Product)', readonly=False)

    sh_product_bm_is_virtual_available = fields.Boolean(
        related='company_id.sh_product_bm_is_virtual_available', string='Show Forecast Quantity? (Product)', readonly=False)
