# -*- coding: utf-8 -*-
# from odoo import http


# class ThemaPriopioDac(http.Controller):
#     @http.route('/thema_priopio__dac/thema_priopio__dac', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/thema_priopio__dac/thema_priopio__dac/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('thema_priopio__dac.listing', {
#             'root': '/thema_priopio__dac/thema_priopio__dac',
#             'objects': http.request.env['thema_priopio__dac.thema_priopio__dac'].search([]),
#         })

#     @http.route('/thema_priopio__dac/thema_priopio__dac/objects/<model("thema_priopio__dac.thema_priopio__dac"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('thema_priopio__dac.object', {
#             'object': obj
#         })
