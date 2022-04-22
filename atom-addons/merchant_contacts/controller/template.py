# -*- coding: utf-8 -*-

# File: template.py	
# Created at 24/11/2021

"""
   Description: 
        -
        -
"""
from odoo import http


class TemplateController(http.Controller):

    @http.route('/merchant_contact', auth='public')
    def index(self, **kw):
        print('[debug] call template')
        value = {}
        value['user'] = "Như cứt >........."
        self.env['project'].create({

        })
        return http.request.render('merchant_contacts.template_test', {
            'teacher': value
        })
