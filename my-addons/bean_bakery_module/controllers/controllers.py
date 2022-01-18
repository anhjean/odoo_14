# -*- coding: utf-8 -*-
# from odoo import http


# class First-module(http.Controller):
#     @http.route('/first-module/first-module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/first-module/first-module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('first-module.listing', {
#             'root': '/first-module/first-module',
#             'objects': http.request.env['first-module.first-module'].search([]),
#         })

#     @http.route('/first-module/first-module/objects/<model("first-module.first-module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('first-module.object', {
#             'object': obj
#         })
