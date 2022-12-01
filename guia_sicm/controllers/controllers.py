# -*- coding: utf-8 -*-
# from odoo import http


# class GuiaSicm(http.Controller):
#     @http.route('/guia_sicm/guia_sicm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/guia_sicm/guia_sicm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('guia_sicm.listing', {
#             'root': '/guia_sicm/guia_sicm',
#             'objects': http.request.env['guia_sicm.guia_sicm'].search([]),
#         })

#     @http.route('/guia_sicm/guia_sicm/objects/<model("guia_sicm.guia_sicm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('guia_sicm.object', {
#             'object': obj
#         })
