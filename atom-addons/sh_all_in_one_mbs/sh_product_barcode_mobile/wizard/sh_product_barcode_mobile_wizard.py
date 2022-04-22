# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import api, fields, models, _


class ShProductBarcodeMobileWizard(models.TransientModel):
    _name = "sh.product.barcode.mobile.wizard"
    _description = "Get Price Mobile Barcode Scanner"

    name = fields.Char(string="Name", default="Product details")

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id.id, required=True)

    post_msg = fields.Html(
        'Message', translate=True,
        help='Message displayed after having scan product')

    def default_sh_product_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_product_bm_is_cont_scan

    sh_product_barcode_mobile = fields.Char(string="Mobile Barcode")

    sh_product_bm_is_cont_scan = fields.Char(
        string='Continuously Scan?', default=default_sh_product_bm_is_cont_scan, readonly=True)

    @api.onchange('sh_product_barcode_mobile')
    def _onchange_sh_product_barcode_mobile(self):

        if self.sh_product_barcode_mobile in ['', "", False, None]:
            return

        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_product_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"

        if self.env.user.company_id.sudo().sh_product_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"

        if self and self.sh_product_barcode_mobile:
            domain = []
            if self.env.user.company_id.sudo().sh_product_barcode_mobile_type == "barcode":
                domain = [("barcode", "=", self.sh_product_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_product_barcode_mobile_type == "int_ref":
                domain = [("default_code", "=", self.sh_product_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_product_barcode_mobile_type == "sh_qr_code":
                domain = [("sh_qr_code", "=", self.sh_product_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_product_barcode_mobile_type == "all":
                domain = ["|", "|",
                          ("default_code", "=", self.sh_product_barcode_mobile),
                          ("barcode", "=", self.sh_product_barcode_mobile),
                          ("sh_qr_code", "=", self.sh_product_barcode_mobile)
                          ]

            search_product = self.env["product.product"].search(
                domain, limit=1)
            if search_product:

                msg = '''<div><h4>
                Product: <font color="red">%(display_name)s </font>
                ''' % {
                    'display_name': search_product.display_name,
                }

                if self.env.user.company_id.sudo().sh_product_bm_is_default_code:
                    msg += '''
                    <br/><br/>
                    Internal Reference: <font color="red">%(default_code)s </font>                   
                    ''' % {
                        'default_code': search_product.default_code or '',
                    }

                if self.env.user.company_id.sudo().sh_product_bm_is_lst_price:
                    msg += '''
                    <br/><br/>
                    Sale Price: <font color="red">%(lst_price)s </font>                 
                    ''' % {
                        'lst_price': search_product.lst_price,
                    }

                if self.env.user.company_id.sudo().sh_product_bm_is_qty_available and search_product.type == 'product':
                    msg += '''
                    <br/><br/>
                    Quantity On Hand: <font color="red">%(qty_available)s </font>             
                    ''' % {
                        'qty_available': search_product.qty_available,
                    }

                if self.env.user.company_id.sudo().sh_product_bm_is_virtual_available and search_product.type == 'product':
                    msg += '''
                    <br/><br/>
                    Forecast Quantity: <font color="red">%(virtual_available)s </font>        
                    ''' % {
                        'virtual_available': search_product.virtual_available,
                    }

                msg += '''
                </div></h4>
                '''

                self.post_msg = msg

                if self.env.user.company_id.sudo().sh_product_bm_is_notify_on_success:
                    message = _(CODE_SOUND_SUCCESS +
                                'Product: %s') % (search_product.display_name)
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner',
                         self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})

            else:
                self.post_msg = False

                if self.env.user.company_id.sudo().sh_product_bm_is_notify_on_fail:
                    message = _(
                        CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner',
                         self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
