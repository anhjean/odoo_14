# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_invoice_barcode_mobile_type = fields.Selection(
        related='company_id.sh_invoice_barcode_mobile_type', string='Product Scan Options In Mobile (Invoice)', translate=True, readonly=False)

    sh_invoice_bm_is_cont_scan = fields.Boolean(
        related='company_id.sh_invoice_bm_is_cont_scan', string='Continuously Scan? (Invoice)', readonly=False)

    sh_invoice_bm_is_notify_on_success = fields.Boolean(
        related='company_id.sh_invoice_bm_is_notify_on_success', string='Notification On Product Succeed? (Invoice)', readonly=False)

    sh_invoice_bm_is_notify_on_fail = fields.Boolean(
        related='company_id.sh_invoice_bm_is_notify_on_fail', string='Notification On Product Failed? (Invoice)', readonly=False)

    sh_invoice_bm_is_sound_on_success = fields.Boolean(
        related='company_id.sh_invoice_bm_is_sound_on_success', string='Play Sound On Product Succeed? (Invoice)', readonly=False)

    sh_invoice_bm_is_sound_on_fail = fields.Boolean(
        related='company_id.sh_invoice_bm_is_sound_on_fail', string='Play Sound On Product Failed? (Invoice)', readonly=False)
