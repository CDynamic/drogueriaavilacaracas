# -*- coding: utf-8 -*-
# from odoo import http


# class SettingInitialAccounting(http.Controller):
#     @http.route('/setting_initial_accounting/setting_initial_accounting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/setting_initial_accounting/setting_initial_accounting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('setting_initial_accounting.listing', {
#             'root': '/setting_initial_accounting/setting_initial_accounting',
#             'objects': http.request.env['setting_initial_accounting.setting_initial_accounting'].search([]),
#         })

#     @http.route('/setting_initial_accounting/setting_initial_accounting/objects/<model("setting_initial_accounting.setting_initial_accounting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('setting_initial_accounting.object', {
#             'object': obj
#         })
