# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Global Search Document
    sh_global_document_search_is_enable = fields.Boolean(
        related='company_id.sh_global_document_search_is_enable', string='Enable global document search', readonly=False)
    
    sh_global_document_search_is_sale = fields.Boolean(
        related='company_id.sh_global_document_search_is_sale', string='Sale Order Search', readonly=False)

    sh_global_document_search_is_purchase = fields.Boolean(
        related='company_id.sh_global_document_search_is_purchase', string='Purchase Order Search', readonly=False)

    sh_global_document_search_is_picking = fields.Boolean(
        related='company_id.sh_global_document_search_is_picking', string='Picking Order Search', readonly=False)

    sh_global_document_search_is_invoice = fields.Boolean(
        related='company_id.sh_global_document_search_is_invoice', string='Invoice Order Search', readonly=False)

    sh_global_document_search_is_product = fields.Boolean(
        related='company_id.sh_global_document_search_is_product', string='Product Search', readonly=False)

    sh_global_document_search_is_lot = fields.Boolean(
        related='company_id.sh_global_document_search_is_lot', string='Lots/Serial Number Search', readonly=False)

    sh_global_document_search_is_location = fields.Boolean(
        related='company_id.sh_global_document_search_is_location', string='Location Search', readonly=False)

    sh_global_document_search_action_target_type = fields.Selection(related='company_id.sh_global_document_search_action_target_type',string='Document Open Mode', translate=True,readonly = False)
    