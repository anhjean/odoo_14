# -*- coding: utf-8 -*-

# File: res_partner.py	
# Created at 07/12/2021

"""
   Description: 
        -
        -
"""


from odoo import http


class TemplateController(http.Controller):

    @http.route('/merchant_contact', auth='public')
    def index(self, **kw):
        value = {}
        value['user'] = "Như cứt >........."
        self.env['project'].create({

        })
        return http.request.render('merchant_contacts.template_test', {
            'teacher': value
        })
