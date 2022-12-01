# -*- coding: utf-8 -*-
# from odoo import http


# class Ctdac(http.Controller):
#     @http.route('/ctdac/ctdac', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ctdac/ctdac/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ctdac.listing', {
#             'root': '/ctdac/ctdac',
#             'objects': http.request.env['ctdac.ctdac'].search([]),
#         })

#     @http.route('/ctdac/ctdac/objects/<model("ctdac.ctdac"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ctdac.object', {
#             'object': obj
#         })
