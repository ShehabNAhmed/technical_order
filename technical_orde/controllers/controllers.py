# -*- coding: utf-8 -*-
# from odoo import http


# class TechnicalOrde(http.Controller):
#     @http.route('/technical_orde/technical_orde', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/technical_orde/technical_orde/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('technical_orde.listing', {
#             'root': '/technical_orde/technical_orde',
#             'objects': http.request.env['technical_orde.technical_orde'].search([]),
#         })

#     @http.route('/technical_orde/technical_orde/objects/<model("technical_orde.technical_orde"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('technical_orde.object', {
#             'object': obj
#         })
