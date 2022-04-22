# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import models, fields, api, _


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.model
    def default_sh_bom_bm_is_cont_scan(self):
        return self.env.company.sh_bom_bm_is_cont_scan

    sh_bom_barcode_mobile = fields.Char(string="Mobile Barcode")

    sh_bom_bm_is_cont_scan = fields.Char(
        string='Continuously Scan?', default=default_sh_bom_bm_is_cont_scan, readonly=True)

    @api.onchange('sh_bom_barcode_mobile')
    def _onchange_sh_bom_barcode_mobile(self):
        # step 2 increaset product qty by 1 if product not in bom line than create new bom line.

        if self.sh_bom_barcode_mobile in ['', "", False, None]:
            return

        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_bom_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"

        if self.env.user.company_id.sudo().sh_bom_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"

        if self and self.sh_bom_barcode_mobile:
            search_lines = False
            domain = []
            if self.env.user.company_id.sudo().sh_bom_barcode_mobile_type == "barcode":
                search_lines = self.bom_line_ids.filtered(
                    lambda ol: ol.product_id.barcode == self.sh_bom_barcode_mobile)
                domain = [("barcode", "=", self.sh_bom_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_bom_barcode_mobile_type == "int_ref":
                search_lines = self.bom_line_ids.filtered(
                    lambda ol: ol.product_id.default_code == self.sh_bom_barcode_mobile)
                domain = [("default_code", "=", self.sh_bom_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_bom_barcode_mobile_type == "sh_qr_code":
                search_lines = self.bom_line_ids.filtered(
                    lambda ol: ol.product_id.sh_qr_code == self.sh_bom_barcode_mobile)
                domain = [("sh_qr_code", "=", self.sh_bom_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_bom_barcode_mobile_type == "all":
                search_lines = self.bom_line_ids.filtered(lambda ol: ol.product_id.barcode == self.sh_bom_barcode_mobile
                                                          or ol.product_id.default_code == self.sh_bom_barcode_mobile
                                                          or ol.product_id.sh_qr_code == self.sh_bom_barcode_mobile)
                domain = ["|", "|",
                          ("default_code", "=", self.sh_bom_barcode_mobile),
                          ("barcode", "=", self.sh_bom_barcode_mobile),
                          ("sh_qr_code", "=", self.sh_bom_barcode_mobile),
                          ]
            if search_lines:
                for line in search_lines:
                    line.product_qty += 1
                    line.onchange_product_id()

                    if self.env.user.company_id.sudo().sh_bom_bm_is_notify_on_success:
                        message = _(
                            CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name, line.product_qty)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                    break
            else:
                search_product = self.env["product.product"].search(
                    domain, limit=1)
                if search_product:

                    bom_line_val = {
                        "product_id": search_product.id,
                        "product_qty": 1,
                    }
                    if search_product.uom_id:
                        bom_line_val.update({
                            "product_uom_id": search_product.uom_id.id,
                        })

                    new_order_line = self.bom_line_ids.new(bom_line_val)
                    self.bom_line_ids += new_order_line
                    new_order_line.onchange_product_id()

                    if self.env.user.company_id.sudo().sh_bom_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (
                            new_order_line.product_id.name, new_order_line.product_qty)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                else:
                    if self.env.user.company_id.sudo().sh_bom_bm_is_notify_on_fail:
                        message = _(
                            CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
