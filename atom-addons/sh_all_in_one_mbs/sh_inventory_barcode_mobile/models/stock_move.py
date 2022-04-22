# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    sh_stock_move_barcode_mobile = fields.Char(string="Mobile Barcode")

    @api.model
    def default_sh_stock_move_bm_is_cont_scan(self):
        return self.env.company.sh_stock_bm_is_cont_scan

    sh_stock_move_bm_is_cont_scan = fields.Char(
        string='Continuously Scan?', default=default_sh_stock_move_bm_is_cont_scan, readonly=True)

    def sh_stock_move_barcode_mobile_has_tracking(self, CODE_SOUND_SUCCESS, CODE_SOUND_FAIL):
        barcode = self.sh_stock_move_barcode_mobile

        if self.picking_code == 'incoming':
            # FOR PURCHASE
            # LOT PRODUCT
            if self.product_id.tracking == 'lot':
                #First Time Scan
                lines = self.move_line_nosuggest_ids.filtered(
                    lambda r: r.lot_name == False)
                if lines:
                    for line in lines:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        vals_line = {
                            'qty_done': qty_done,
                            'lot_name': barcode,
                        }
                        self.update({
                            'move_line_nosuggest_ids': [(1, line.id, vals_line)]
                        })
                        # odoo v14 update below way

                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                self.product_id.name, line.qty_done, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                        break
                else:
                    #Second Time Scan
                    lines = self.move_line_nosuggest_ids.filtered(
                        lambda r: r.lot_name == barcode)
                    if lines:
                        for line in lines:
                            # odoo v14 update below way
                            qty_done = line.qty_done + 1
                            vals_line = {
                                'qty_done': qty_done,
                            }
                            self.update({
                                'move_line_nosuggest_ids': [(1, line.id, vals_line)]
                            })
                            # odoo v14 update below way

                            # success message here
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                                message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                    self.product_id.name, line.qty_done, barcode)
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                            break

                    else:
                        #New Barcode Scan then create new line
                        vals_line = {
                            'product_id': self.product_id.id,
                            'location_dest_id': self.location_dest_id.id,
                            'lot_name': barcode,
                            'qty_done': 1,
                            'product_uom_id': self.product_uom.id,
                            'location_id': self.location_id.id,
                        }
                        self.update({
                            'move_line_nosuggest_ids': [(0, 0, vals_line)]
                        })

                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                self.product_id.name, 1, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

            # SERIAL PRODUCT
            if self.product_id.tracking == 'serial':
                #VALIDATION SERIAL NO. ALREADY EXIST.
                lines = self.move_line_nosuggest_ids.filtered(
                    lambda r: r.lot_name == barcode)
                if lines:
                    # failed message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(CODE_SOUND_FAIL +
                                    'Serial Number already exist!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                    return

                #First Time Scan
                lines = self.move_line_nosuggest_ids.filtered(
                    lambda r: r.lot_name == False)
                if lines:
                    for line in lines:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        vals_line = {
                            'qty_done': qty_done,
                            'lot_name': barcode
                        }
                        self.update({
                            'move_line_nosuggest_ids': [(1, line.id, vals_line)]
                        })
                        # odoo v14 update below way

                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                self.product_id.name, line.qty_done, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                        break
                else:
                    #Create new line if not found any unallocated serial number line
                    vals_line = {
                        'product_id': self.product_id.id,
                        'location_dest_id': self.location_dest_id.id,
                        'lot_name': barcode,
                        'qty_done': 1,
                        'product_uom_id': self.product_uom.id,
                        'location_id': self.location_id.id,
                    }
                    self.update({
                        'move_line_nosuggest_ids': [(0, 0, vals_line)]
                    })

                    # success message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                            self.product_id.name, 1, barcode)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

            quantity_done = 0
            for move_line in self.move_line_nosuggest_ids:
                quantity_done += move_line.product_uom_id._compute_quantity(
                    move_line.qty_done, self.product_uom, round=False)

            if quantity_done == self.product_uom_qty + 1:
                # failed message here
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(
                        CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner',
                         self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                return
        elif self and self.picking_code in ['outgoing', 'internal']:
            # FOR SALE
            # LOT PRODUCT
            quant_obj = self.env['stock.quant']

            # FOR LOT PRODUCT
            if self.product_id.tracking == 'lot':
                #First Time Scan
                quant = quant_obj.search([
                    ('product_id', '=', self.product_id.id),
                    ('quantity', '>', 0),
                    ('location_id.usage', '=', 'internal'),
                    ('lot_id.name', '=', barcode),
                    ('location_id', 'child_of', self.location_id.id)
                ], limit=1)

                if not quant:
                    # failed message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(
                            CODE_SOUND_FAIL + 'There are no available qty for this lot: %s') % (barcode)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                    return

                lines = self.move_line_ids.filtered(
                    lambda r: r.lot_id == False)
                if lines:
                    for line in lines:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        vals_line = {
                            'qty_done': qty_done,
                            'lot_id': quant.lot_id.id
                        }
                        self.update({
                            'move_line_ids': [(1, line.id, vals_line)]
                        })
                        # odoo v14 update below way

                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                self.product_id.name, line.qty_done, quant.lot_id.name)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                        break
                else:
                    #Second Time Scan
                    lines = self.move_line_ids.filtered(
                        lambda r: r.lot_id.name == barcode)
                    if lines:
                        for line in lines:
                            # odoo v14 update below way
                            qty_done = line.qty_done + 1
                            vals_line = {
                                'qty_done': qty_done,
                            }
                            self.update({
                                'move_line_ids': [(1, line.id, vals_line)]
                            })
                            # odoo v14 update below way

                            # success message here
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                                message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                    self.product_id.name, line.qty_done, quant.lot_id.name)
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                            break
                    else:
                        #New Barcode Scan then create new line
                        vals_line = {
                            'product_id': self.product_id.id,
                            'location_dest_id': self.location_dest_id.id,
                            'lot_id': quant.lot_id.id,
                            'qty_done': 1,
                            'product_uom_id': self.product_uom.id,
                            'location_id': quant.location_id.id,
                        }
                        self.update({
                            'move_line_ids': [(0, 0, vals_line)]
                        })
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                self.product_id.name, 1, quant.lot_id.name)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
            # FOR SERIAL PRODUCT
            if self.product_id.tracking == 'serial':
                #First Time Scan
                lines = self.move_line_ids.filtered(
                    lambda r: r.lot_id.name == barcode)
                if lines:
                    for line in lines:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        vals_line = {
                            'qty_done': qty_done,
                        }
                        self.update({
                            'move_line_ids': [(1, line.id, vals_line)]
                        })
                        # odoo v14 update below way

                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                                self.product_id.name, line.qty_done, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                        if float_compare(line.qty_done, 1.0, precision_rounding=line.product_id.uom_id.rounding) != 0:
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(
                                    CODE_SOUND_FAIL + 'You can only process 1.0 %s of products with unique serial number.') % line.product_id.uom_id.name
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                        break
                else:
                    list_allocated_serial_ids = []
                    if self.move_line_ids:
                        for line in self.move_line_ids:
                            if line.lot_id:
                                list_allocated_serial_ids.append(
                                    line.lot_id.id)

                    # if need new line.
                    quant = quant_obj.search([
                        ('product_id', '=', self.product_id.id),
                        ('quantity', '>', 0),
                        ('location_id.usage', '=', 'internal'),
                        ('lot_id.name', '=', barcode),
                        ('location_id', 'child_of', self.location_id.id),
                        ('lot_id.id', 'not in', list_allocated_serial_ids),
                    ], limit=1)

                    if not quant:
                        #                         raise UserError(_("There are no available qty for this lot/serial."))
                        # failed message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'There are no available qty for this lot/serial: %s') % (barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                        return

                    #New Barcode Scan then create new line
                    vals_line = {
                        'product_id': self.product_id.id,
                        'location_dest_id': self.location_dest_id.id,
                        'lot_id': quant.lot_id.id,
                        'qty_done': 1,
                        'product_uom_id': self.product_uom.id,
                        'location_id': quant.location_id.id,
                    }
                    self.update({
                        'move_line_ids': [(0, 0, vals_line)]
                    })

                    # success message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (
                            self.product_id.name, 1, quant.lot_id.name)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

            quantity_done = 0
            for move_line in self._get_move_lines():
                quantity_done += move_line.product_uom_id._compute_quantity(
                    move_line.qty_done, self.product_uom, round=False)

            if self.picking_code == 'outgoing' and quantity_done == self.product_uom_qty + 1:
                # failed message here
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(
                        CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner',
                         self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})
                return
        else:
            # failed message here
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(
                    CODE_SOUND_FAIL + 'Picking type is not outgoing or incoming or internal transfer.')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

    def sh_stock_move_barcode_mobile_no_tracking(self, CODE_SOUND_SUCCESS, CODE_SOUND_FAIL):
        move_lines = False

        # INCOMING
        # ===================================
        if self.picking_code in ['incoming']:
            move_lines = self.move_line_nosuggest_ids

        # OUTGOING AND TRANSFER
        # ===================================
        elif self.picking_code in ['outgoing', 'internal']:
            move_lines = self.move_line_ids

        if move_lines:
            for line in move_lines:
                if self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'barcode':
                    if self.product_id.barcode == self.sh_stock_move_barcode_mobile:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        if self.picking_code in ['incoming']:
                            self.update({
                                'move_line_nosuggest_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        if self.picking_code in ['outgoing', 'internal']:
                            self.update({
                                'move_line_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        # odoo v14 update below way
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(
                                CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name, line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                        if self.quantity_done == self.product_uom_qty + 1:
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(
                                    CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                        break
                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                        return

                elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'int_ref':
                    if self.product_id.default_code == self.sh_stock_move_barcode_mobile:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        if self.picking_code in ['incoming']:
                            self.update({
                                'move_line_nosuggest_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        if self.picking_code in ['outgoing', 'internal']:
                            self.update({
                                'move_line_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        # odoo v14 update below way
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(
                                CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name, line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                        if self.quantity_done == self.product_uom_qty + 1:
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(
                                    CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                        break
                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                        return

                elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'sh_qr_code':
                    if self.product_id.sh_qr_code == self.sh_stock_move_barcode_mobile:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        if self.picking_code in ['incoming']:
                            self.update({
                                'move_line_nosuggest_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        if self.picking_code in ['outgoing', 'internal']:
                            self.update({
                                'move_line_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        # odoo v14 update below way
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(
                                CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name, line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                        if self.quantity_done == self.product_uom_qty + 1:
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(
                                    CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                        break
                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                        return

                elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'all':

                    if self.product_id.barcode == self.sh_stock_move_barcode_mobile or self.product_id.default_code == self.sh_stock_move_barcode_mobile or self.product_id.sh_qr_code == self.sh_stock_move_barcode_mobile:
                        # odoo v14 update below way
                        qty_done = line.qty_done + 1
                        if self.picking_code in ['incoming']:
                            self.update({
                                'move_line_nosuggest_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        if self.picking_code in ['outgoing', 'internal']:
                            self.update({
                                'move_line_ids': [(1, line.id, {'qty_done': qty_done})]
                            })
                        # odoo v14 update below way
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(
                                CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name, line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                        if self.quantity_done == self.product_uom_qty + 1:
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(
                                    CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})

                        break
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
                message = _(CODE_SOUND_FAIL +
                            'Pls add all product items in line than rescan.')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

            return

    @api.onchange('sh_stock_move_barcode_mobile')
    def _onchange_sh_stock_move_barcode_mobile(self):

        if self.sh_stock_move_barcode_mobile in ['', "", False, None]:
            return

        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"

        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"

        if self.picking_id.state not in ['confirmed', 'assigned']:
            selections = self.picking_id.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] ==
                          self.picking_id.state), self.picking_id.state)
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL +
                            'You can not scan item in %s state.') % (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

            return

        if self.sh_stock_move_barcode_mobile:
            if self.has_tracking != 'none':
                self.sh_stock_move_barcode_mobile_has_tracking(
                    CODE_SOUND_SUCCESS, CODE_SOUND_FAIL)

            else:
                self.sh_stock_move_barcode_mobile_no_tracking(
                    CODE_SOUND_SUCCESS, CODE_SOUND_FAIL)
