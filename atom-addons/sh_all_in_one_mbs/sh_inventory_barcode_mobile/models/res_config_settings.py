# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_stock_barcode_mobile_type = fields.Selection(string='Product Scan Options In Mobile (Stock Picking)',
                                                    related="company_id.sh_stock_barcode_mobile_type", translate=True, readonly=False)

    sh_stock_bm_is_cont_scan = fields.Boolean(
        string='Continuously Scan? (Stock Picking)', related="company_id.sh_stock_bm_is_cont_scan", readonly=False)

    sh_stock_bm_is_notify_on_success = fields.Boolean(
        string='Notification On Product Succeed? (Stock Picking)', related="company_id.sh_stock_bm_is_notify_on_success", readonly=False)

    sh_stock_bm_is_notify_on_fail = fields.Boolean(
        string='Notification On Product Failed? (Stock Picking)', related="company_id.sh_stock_bm_is_notify_on_fail", readonly=False)

    sh_stock_bm_is_sound_on_success = fields.Boolean(
        string='Play Sound On Product Succeed? (Stock Picking)', related="company_id.sh_stock_bm_is_sound_on_success", readonly=False)

    sh_stock_bm_is_sound_on_fail = fields.Boolean(
        string='Play Sound On Product Failed? (Stock Picking)', related="company_id.sh_stock_bm_is_sound_on_fail", readonly=False)

    sh_stock_bm_is_add_product = fields.Boolean(
        string="Is add new product in picking? (Stock Picking)", related="company_id.sh_stock_bm_is_add_product", readonly=False)
