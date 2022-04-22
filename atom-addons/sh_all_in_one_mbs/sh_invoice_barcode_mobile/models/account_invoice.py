# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_taxes_invoice_lines(self, move_id):
        self.ensure_one()

        tax_ids = None
        if move_id.is_sale_document(include_receipts=True):
            # Out invoice.
            if self.product_id.taxes_id:
                tax_ids = self.product_id.taxes_id.filtered(
                    lambda tax: tax.company_id == move_id.company_id)
            elif self.account_id.tax_ids:
                tax_ids = self.account_id.tax_ids
            else:
                tax_ids = self.env['account.tax']
            if not tax_ids and not self.exclude_from_invoice_tab:
                tax_ids = move_id.company_id.account_sale_tax_id
        elif move_id.is_purchase_document(include_receipts=True):
            # In invoice.
            if self.product_id.supplier_taxes_id:
                tax_ids = self.product_id.supplier_taxes_id.filtered(
                    lambda tax: tax.company_id == move_id.company_id)
            elif self.account_id.tax_ids:
                tax_ids = self.account_id.tax_ids
            else:
                tax_ids = self.env['account.tax']
            if not tax_ids and not self.exclude_from_invoice_tab:
                tax_ids = move_id.company_id.account_purchase_tax_id
        else:
            # Miscellaneous operation.
            tax_ids = self.account_id.tax_ids

        if self.company_id and tax_ids:
            tax_ids = tax_ids.filtered(
                lambda tax: tax.company_id == self.company_id)

        fiscal_position = move_id.fiscal_position_id
        if tax_ids and fiscal_position:
            return fiscal_position.map_tax(tax_ids, partner=self.partner_id)
        else:
            return tax_ids


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["barcodes.barcode_events_mixin", "account.move"]

    @api.model
    def _get_tax_grouping_key_from_base_line(self, base_line, tax_vals):
        ''' Create the dictionary based on a base line that will be used as key to group taxes together.
        /!\ Must be consistent with '_get_tax_grouping_key_from_tax_line'.
        :param base_line:   An account.move.line being a base line (that could contains something in 'tax_ids').
        :param tax_vals:    An element of compute_all(...)['taxes'].
        :return:            A dictionary containing all fields on which the tax will be grouped.
        '''
        tax_repartition_line = self.env['account.tax.repartition.line'].browse(
            tax_vals['tax_repartition_line_id'])
        account = base_line._get_default_tax_account(
            tax_repartition_line) or base_line.account_id
        return {
            'tax_repartition_line_id': tax_vals['tax_repartition_line_id'],
            'account_id': account.id,
            'currency_id': base_line.currency_id.id or self.currency_id.id,
            'analytic_tag_ids': [(6, 0, tax_vals['analytic'] and base_line.analytic_tag_ids.ids or [])],
            'analytic_account_id': tax_vals['analytic'] and base_line.analytic_account_id.id,
            'tax_ids': [(6, 0, tax_vals['tax_ids'])],
            'tax_tag_ids': [(6, 0, tax_vals['tag_ids'])],
        }

    @api.model
    def default_sh_invoice_bm_is_cont_scan(self):
        return self.env.company.sh_invoice_bm_is_cont_scan

    sh_invoice_barcode_mobile = fields.Char(string="Mobile Barcode")

    sh_invoice_bm_is_cont_scan = fields.Char(
        string='Continuously Scan?', default=default_sh_invoice_bm_is_cont_scan, readonly=True)

    def write(self, vals):
        res = False
        for rec in self:
            if self.env.context.get('check_move_validity') != False:
                res = super(AccountMove, self).with_context(
                    check_move_validity=False).write(vals)
            else:
                res = super(AccountMove, self).write(vals)

        if not res:
            res = super(AccountMove, self).write(vals)
            return res

        return res

    @api.model
    def create(self, vals):
        res = False
        if self.env.context.get('check_move_validity') != False:
            res = super(AccountMove, self).with_context(
                check_move_validity=False).create(vals)
        else:
            res = super(AccountMove, self).create(vals)

        if not res:
            res = super(AccountMove, self).create(vals)
            return res

        return res

    @api.onchange('sh_invoice_barcode_mobile')
    def _onchange_sh_invoice_barcode_mobile(self):

        if self.sh_invoice_barcode_mobile in ['', "", False, None]:
            return

        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_invoice_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"

        if self.env.user.company_id.sudo().sh_invoice_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"

        if self and self.state != "draft":
            selections = self.fields_get()["state"]["selection"]
            value = next((v[1] for v in selections if v[0]
                          == self.state), self.state)

            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL +
                            'You can not scan item in %s state.') % (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

            return

        # step 2 increaset product qty by 1 if product not in order line than create new order line.
        elif self:
            search_lines = False
            domain = []
            if self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "barcode":
                search_lines = self.invoice_line_ids.filtered(
                    lambda ol: ol.product_id.barcode == self.sh_invoice_barcode_mobile)
                domain = [("barcode", "=", self.sh_invoice_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "int_ref":
                search_lines = self.invoice_line_ids.filtered(
                    lambda ol: ol.product_id.default_code == self.sh_invoice_barcode_mobile)
                domain = [("default_code", "=", self.sh_invoice_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "sh_qr_code":
                search_lines = self.invoice_line_ids.filtered(
                    lambda ol: ol.product_id.sh_qr_code == self.sh_invoice_barcode_mobile)
                domain = [("sh_qr_code", "=", self.sh_invoice_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "all":
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.barcode == self.sh_invoice_barcode_mobile
                                                              or ol.product_id.default_code == self.sh_invoice_barcode_mobile
                                                              or ol.product_id.sh_qr_code == self.sh_invoice_barcode_mobile)
                domain = ["|", "|",
                          ("default_code", "=", self.sh_invoice_barcode_mobile),
                          ("barcode", "=", self.sh_invoice_barcode_mobile),
                          ("sh_qr_code", "=", self.sh_invoice_barcode_mobile)

                          ]

            if search_lines:
                for line in search_lines:
                    line.quantity += 1
                    line._onchange_product_id()
                    line._onchange_price_subtotal()

                    if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_success:
                        message = _(
                            CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name, line.quantity)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                    break
                self._compute_invoice_taxes_by_group()
                self._onchange_invoice_line_ids()
                self._compute_amount()
                self._recompute_dynamic_lines(recompute_all_taxes=True)

            else:
                search_product = self.env["product.product"].search(
                    domain, limit=1)
                if search_product:
                    ir_property_obj = self.env['ir.property']
                    account_id = False

                    if self.move_type in ['out_invoice', 'out_refund']:
                        account_id = search_product.property_account_income_id.id or search_product.categ_id.property_account_income_categ_id.id
                        if not account_id:
                            inc_acc = ir_property_obj.get(
                                'property_account_income_categ_id', 'product.category')
                            account_id = self.fiscal_position_id.map_account(
                                inc_acc).id if inc_acc else False
                        if not account_id:
                            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                                message = _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') % (
                                    search_product.name)
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            return

                    if self.move_type in ['in_invoice', 'in_refund']:
                        account_id = search_product.property_account_expense_id.id or search_product.categ_id.property_account_expense_categ_id.id
                        if not account_id:
                            inc_acc = ir_property_obj.get(
                                'property_account_expense_categ_id', 'product.category')
                            account_id = self.fiscal_position_id.map_account(
                                inc_acc).id if inc_acc else False
                        if not account_id:
                            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                                message = _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') % (
                                    search_product.name)
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner',
                                     self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

                            return

                    invoice_line_val = {
                        "name": search_product.name,
                        "product_id": search_product.id,
                        "quantity": 1,
                        'account_id': account_id,
                    }

                    if self.move_type in ['out_invoice', 'out_refund']:
                        invoice_line_val.update({
                            "price_unit": search_product.lst_price
                        })

                    elif self.move_type in ['in_invoice', 'in_refund']:
                        invoice_line_val.update({
                            "price_unit": search_product.standard_price
                        })

                    invoice_line_val.update({'move_id': self})

                    if self.move_type in ['out_invoice', 'out_refund']:
                        if search_product.taxes_id:
                            invoice_line_val.update({'tax_ids': [(6, 0, search_product.taxes_id.filtered(
                                lambda tax: tax.company_id == self.company_id).ids)]})
                    elif self.move_type in ['in_invoice', 'in_refund']:
                        if search_product.supplier_taxes_id:
                            invoice_line_val.update({'tax_ids': [(6, 0, search_product.supplier_taxes_id.filtered(
                                lambda tax: tax.company_id == self.company_id).ids)]})
#
                    if search_product.uom_id:
                        invoice_line_val.update({
                            "product_uom_id": search_product.uom_id.id,
                        })

                    # create
                    self.update(
                        {'invoice_line_ids': [(0, 0, invoice_line_val)]})

                    for rec in self.invoice_line_ids:
                        rec._onchange_product_id()
                        rec._onchange_price_subtotal()

                    self._compute_invoice_taxes_by_group()
                    self._onchange_invoice_line_ids()
                    self._compute_amount()
                    self._recompute_dynamic_lines(recompute_all_taxes=True)

                    if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_success:
                        message = _(
                            CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (search_product.name, 1)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                else:
                    if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                        message = _(
                            CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
