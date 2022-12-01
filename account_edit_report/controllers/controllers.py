# -*- coding: utf-8 -*-
# from odoo import http


# class AccountEditReport(http.Controller):
#     @http.route('/account_edit_report/account_edit_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_edit_report/account_edit_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_edit_report.listing', {
#             'root': '/account_edit_report/account_edit_report',
#             'objects': http.request.env['account_edit_report.account_edit_report'].search([]),
#         })

#     @http.route('/account_edit_report/account_edit_report/objects/<model("account_edit_report.account_edit_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_edit_report.object', {
#             'object': obj
#         })
