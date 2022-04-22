# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def default_sh_stock_bm_is_cont_scan(self):
        return self.env.company.sh_stock_bm_is_cont_scan

    sh_stock_barcode_mobile = fields.Char(string="Mobile Barcode")

    sh_stock_bm_is_cont_scan = fields.Char(
        string='Continuously Scan?', default=default_sh_stock_bm_is_cont_scan, readonly=True)

    @api.onchange('sh_stock_barcode_mobile')
    def _onchange_sh_stock_barcode_mobile(self):

        if self.sh_stock_barcode_mobile in ['', "", False, None]:
            return

        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"

        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"

        if not self.picking_type_id:
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL +
                            'You must first select a Operation Type.')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

            return

        if self and self.state not in ['assigned', 'draft', 'confirmed']:
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0]
                          == self.state), self.state)
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL +
                            'You can not scan item in %s state.') % (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
            return

#         elif self and self.picking_type_code in ['outgoing','internal']:
#             search_mls = False
#             domain = []
#
#             if self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'barcode':
#                 search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile)
#                 domain = [("barcode","=",self.sh_stock_barcode_mobile)]
#
#             elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'int_ref':
#                 search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.default_code == self.sh_stock_barcode_mobile)
#                 domain = [("default_code","=",self.sh_stock_barcode_mobile)]
#
#             elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'sh_qr_code':
#                 search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.sh_qr_code == self.sh_stock_barcode_mobile)
#                 domain = [("sh_qr_code","=",self.sh_stock_barcode_mobile)]
#
#             elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'all':
#                 search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile
#                                                                          or ml.product_id.default_code == self.sh_stock_barcode_mobile
#                                                                          or ml.product_id.sh_qr_code == self.sh_stock_barcode_mobile
#                                                                          )
#                 domain = ["|","|",
#                     ("default_code","=",self.sh_stock_barcode_mobile),
#                     ("barcode","=",self.sh_stock_barcode_mobile),
#                     ("sh_qr_code","=",self.sh_stock_barcode_mobile)
#                 ]
#
#             if search_mls:
#                 for move_line in search_mls:
#                     if move_line.show_details_visible:
#                         if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                             message = _(CODE_SOUND_FAIL + 'You can not scan product item for Detailed Operations directly here, Pls click detail button (at end each line) and than rescan your product item.')
#                             self.env['bus.bus'].sendone(
#                                 (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                                 {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
#
#                         return
#
#                     move_line.qty_done += 1
#                     if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
#                         message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (move_line.product_id.name,move_line.qty_done)
#                         self.env['bus.bus'].sendone(
#                             (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                             {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
#                     break
#
#             elif self.state == 'draft':
#                 if self.env.user.company_id.sudo().sh_stock_bm_is_add_product:
#                     search_product = self.env["product.product"].search(domain, limit = 1)
#                     if search_product:
#                         stock_move_line_vals = {
#                            "product_id": search_product.id,
#                            "qty_done" : 1,
#                            "location_id" : self.location_id.id,
#                            "location_dest_id": self.location_dest_id.id,
#                            'date' : self.scheduled_date or fields.date.today(),
#                            'company_id' : self.company_id.id if self.company_id else self.env.user.company_id.id
#                         }
#                         if search_product.uom_id:
#                             stock_move_line_vals.update({
#                                 "product_uom_id": search_product.uom_id.id,
#                             })
#
#                         old_lines = self.move_line_ids_without_package
#                         new_order_line = self.move_line_ids_without_package.create(stock_move_line_vals)
#                         self.move_line_ids_without_package = old_lines + new_order_line
#                         new_order_line.onchange_product_id()
#
#                         if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
#                             message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (new_order_line.product_id.name,new_order_line.product_uom_qty)
#                             self.env['bus.bus'].sendone(
#                                 (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                                 {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
#                         return
#                     else:
#                         if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                             message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
#                             self.env['bus.bus'].sendone(
#                                 (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                                 {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
#                         return
#
#
#                 else:
#                     if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                         message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
#                         self.env['bus.bus'].sendone(
#                             (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                             {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
#
#                     return
#             else:
#                 if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                     message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
#                     self.env['bus.bus'].sendone(
#                         (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                         {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
#
#                 return
#
#
        elif self:
            search_mls = False
            domain = []

            if self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'barcode':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile)
                domain = [("barcode", "=", self.sh_stock_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'int_ref':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.default_code == self.sh_stock_barcode_mobile)
                domain = [("default_code", "=", self.sh_stock_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'sh_qr_code':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.sh_qr_code == self.sh_stock_barcode_mobile)
                domain = [("sh_qr_code", "=", self.sh_stock_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'all':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile or ml.product_id.default_code == self.sh_stock_barcode_mobile)
                domain = ["|", "|",
                          ("default_code", "=", self.sh_stock_barcode_mobile),
                          ("barcode", "=", self.sh_stock_barcode_mobile),
                          ("sh_qr_code", "=", self.sh_stock_barcode_mobile),
                          ]

            if search_mls:
                for move_line in search_mls:
                    if move_line.show_details_visible:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'You can not scan product item for Detailed Operations directly here, Pls click detail button (at end each line) and than rescan your product item.')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                        return

                    move_line.quantity_done += 1
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (
                            move_line.product_id.name, move_line.quantity_done)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                    break
            elif self.state == 'draft':
                if self.env.user.company_id.sudo().sh_stock_bm_is_add_product:

                    search_product = self.env["product.product"].search(
                        domain, limit=1)
                    if search_product:
                        stock_move_vals = {
                            "name": search_product.name,
                            "product_id": search_product.id,
                            "price_unit": search_product.lst_price,
                            "quantity_done": 1,
                            "location_id": self.location_id.id,
                            "location_dest_id": self.location_dest_id.id
                        }
                        if search_product.uom_id:
                            stock_move_vals.update({
                                "product_uom": search_product.uom_id.id,
                            })

                        old_lines = self.move_ids_without_package
                        new_order_line = self.move_ids_without_package.create(
                            stock_move_vals)
                        self.move_ids_without_package = old_lines + new_order_line
                        new_order_line.onchange_product_id()
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (
                                new_order_line.product_id.name, new_order_line.quantity_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                        return

                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                        return

                else:
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(
                            CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                    return

            else:
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(
                        CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner',
                         self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                return
        else:
            # failed message here
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(
                    CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

            return
