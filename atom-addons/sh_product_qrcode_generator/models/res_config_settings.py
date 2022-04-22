# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_sh_product_qrcode_generator_when_create = fields.Boolean(
        string="Is Generate QR Code When Product Create?")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        is_sh_product_qrcode_generator_when_create = self.env["ir.config_parameter"].sudo(
        ).get_param("sh_product_qrcode_generator.is_sh_product_qrcode_generator_when_create")

        res.update({
            'is_sh_product_qrcode_generator_when_create': is_sh_product_qrcode_generator_when_create,
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("sh_product_qrcode_generator.is_sh_product_qrcode_generator_when_create",
                                                         self.is_sh_product_qrcode_generator_when_create or False)
