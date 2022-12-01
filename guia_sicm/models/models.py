# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class guia_sicm(models.Model):
#     _name = 'guia_sicm.guia_sicm'
#     _description = 'guia_sicm.guia_sicm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
