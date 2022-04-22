# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.osv import expression


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    sequence = fields.Integer(string='Sequence', default=0)
    sh_inven_adjt_barcode_scanner_is_last_scanned = fields.Boolean(
        string="Last Scanned?")


class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.inventory']

    def sh_barcode_scanner_get_quantities(self, product):
        """Return quantities group by product_id, location_id, lot_id, package_id and owner_id

        :return: a dict with keys as tuple of group by and quantity as value
        :rtype: dict
        """
        self.ensure_one()
        if self.location_ids:
            domain_loc = [('id', 'child_of', self.location_ids.ids)]
        else:
            domain_loc = [('company_id', '=', self.company_id.id),
                          ('usage', 'in', ['internal', 'transit'])]
        locations_ids = [
            l['id'] for l in self.env['stock.location'].search_read(domain_loc, ['id'])]

        domain = [('company_id', '=', self.company_id.id),
                  ('quantity', '!=', '0'),
                  ('location_id', 'in', locations_ids)]
        if self.prefill_counted_quantity == 'zero':
            domain.append(('product_id.active', '=', True))

        # SOFTHEALER CUSTOM CODE
        if product:
            domain = expression.AND(
                [domain, [('product_id', 'in', product.ids)]])
        # SOFTHEALER CUSTOM CODE

        fields = ['product_id', 'location_id', 'lot_id',
                  'package_id', 'owner_id', 'quantity:sum']
        group_by = ['product_id', 'location_id',
                    'lot_id', 'package_id', 'owner_id']

        quants = self.env['stock.quant'].read_group(
            domain, fields, group_by, lazy=False)
        return {(
            quant['product_id'] and quant['product_id'][0] or False,
            quant['location_id'] and quant['location_id'][0] or False,
            quant['lot_id'] and quant['lot_id'][0] or False,
            quant['package_id'] and quant['package_id'][0] or False,
            quant['owner_id'] and quant['owner_id'][0] or False):
            quant['quantity'] for quant in quants
        }

    def sh_barcode_scanner_get_inventory_lines_values(self, product):
        """Return the values of the inventory lines to create for this inventory.

        :return: a list containing the `stock.inventory.line` values to create
        :rtype: list
        """
        self.ensure_one()
        quants_groups = self.sh_barcode_scanner_get_quantities(product)
        vals = []
        for (product_id, location_id, lot_id, package_id, owner_id), quantity in quants_groups.items():
            line_values = {
                'inventory_id': self.id,
                'product_qty': 0 if self.prefill_counted_quantity == "zero" else quantity,
                'theoretical_qty': quantity,
                'prod_lot_id': lot_id,
                'partner_id': owner_id,
                'product_id': product_id,
                'location_id': location_id,
                'package_id': package_id,
                'sh_inven_adjt_barcode_scanner_is_last_scanned': True,
                'sequence': -1
            }
            line_values['product_uom_id'] = self.env['product.product'].browse(
                product_id).uom_id.id
            vals.append(line_values)
#         if self.exhausted:
#             vals += self._get_exhausted_inventory_lines_vals({(l['product_id'], l['location_id']) for l in vals})
        return vals

    @api.model
    def default_sh_inventory_adjt_bm_is_cont_scan(self):
        return self.env.company.sh_inventory_adjt_bm_is_cont_scan

    sh_inventory_adjt_barcode_mobile = fields.Char(string="Mobile Barcode")

    sh_inventory_adjt_bm_is_cont_scan = fields.Char(
        string='Continuously Scan?', default=default_sh_inventory_adjt_bm_is_cont_scan, readonly=True)

    def action_start_sh_inventory_adjust_barcode_scanning(self):
        self.ensure_one()
        self._action_start()
        self._check_company()
        action_tree = self.action_open_inventory_lines()

        action = {
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('stock.view_inventory_form').id, 'form')],
            'view_mode': 'form',
            'res_id': self.id,
            'name': _(self.name or 'Inventory'),
            'res_model': 'stock.inventory',
            'target': 'current',
        }
        action['context'] = action_tree.get('context', {})
        action['domain'] = action_tree.get('domain', [])
        return action

    @api.onchange('sh_inventory_adjt_barcode_mobile')
    def _onchange_sh_inventory_adjt_barcode_mobile(self):
        if self.sh_inventory_adjt_barcode_mobile in ['', "", False, None]:
            return

        barcode = self.sh_inventory_adjt_barcode_mobile
        domain = []
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""

        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"

        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"

        # step 1: state validation.
        if self and self.state != 'confirm':
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0]
                          == self.state), self.state)

            if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL +
                            'You can not scan item in %s state.') % (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})

            return

        elif self:

            self.line_ids.update({
                'sh_inven_adjt_barcode_scanner_is_last_scanned': False,
                'sequence': 0,
            })

            search_lines = False

            if self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'barcode':
                search_lines = self.line_ids.filtered(
                    lambda l: l.product_id.barcode == barcode)
                domain = [("barcode", "=", barcode)]

            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'int_ref':
                search_lines = self.line_ids.filtered(
                    lambda l: l.product_id.default_code == barcode)
                domain = [("default_code", "=", barcode)]

            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'sh_qr_code':
                search_lines = self.line_ids.filtered(
                    lambda l: l.product_id.sh_qr_code == barcode)
                domain = [("sh_qr_code", "=", barcode)]

            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'all':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == barcode or
                                                      l.product_id.default_code == barcode or
                                                      l.product_id.sh_qr_code == barcode,
                                                      )

                domain = ["|", "|",
                          ("default_code", "=", barcode),
                          ("barcode", "=", barcode),
                          ("sh_qr_code", "=", barcode),
                          ]

            if search_lines:
                for line in search_lines:
                    line.product_qty += 1
                    line.sh_inven_adjt_barcode_scanner_is_last_scanned = True,
                    line.sequence = -1
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_success:
                        message = _(
                            CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name, line.product_qty)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                    break
            else:
                # =========================================
                # Create Inventory Line Here
                domain += [
                    ('type', '=', 'product')
                ]
                product = self.env['product.product'].search(domain, limit=1)
                if product:
                    lines_vals = self.sh_barcode_scanner_get_inventory_lines_values(
                        product)
                    # add sequence and last scanned here
                    if len(lines_vals) == 1:
                        lines_vals[0].update({
                            "product_qty": 1
                        })
                    if not lines_vals:
                        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:
                            message = _(
                                CODE_SOUND_FAIL + 'Could not get values of the inventory lines for this scanned product')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner',
                                 self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                        return
                    line_ids_list = [(0, 0, line_vals)
                                     for line_vals in lines_vals]

                    self.update({
                        'line_ids': line_ids_list
                    })

                    # SHOW SUCCESS MESSAGE HERE
                    message = _(CODE_SOUND_SUCCESS +
                                'Product: %s') % (product.name)
                    if len(lines_vals) == 1:
                        message = _(CODE_SOUND_SUCCESS +
                                    'Product: %s Qty: %s') % (product.name, 1)
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_success:
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

                else:
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:
                        message = _(
                            CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner',
                             self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                    return
