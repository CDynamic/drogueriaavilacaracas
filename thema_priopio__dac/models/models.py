# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class thema_priopio__dac(models.Model):
#     _name = 'thema_priopio__dac.thema_priopio__dac'
#     _description = 'thema_priopio__dac.thema_priopio__dac'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
