# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Global Search Document
    sh_global_document_search_is_enable = fields.Boolean(string='Enable global document search')
    
    sh_global_document_search_is_sale = fields.Boolean(string='Sale Order Search')

    sh_global_document_search_is_purchase = fields.Boolean(string='Purchase Order Search')

    sh_global_document_search_is_picking = fields.Boolean(string='Picking Order Search')

    sh_global_document_search_is_invoice = fields.Boolean(string='Invoice Order Search')

    sh_global_document_search_is_product = fields.Boolean(string='Product Search')

    sh_global_document_search_is_lot = fields.Boolean(string='Lots/Serial Number Search')

    sh_global_document_search_is_location = fields.Boolean(string='Location Search')

    sh_global_document_search_action_target_type = fields.Selection([
        ('current','Current'),
        ('new','New')
        ],default = 'current' ,string='Document Open Mode', translate=True)
        
    