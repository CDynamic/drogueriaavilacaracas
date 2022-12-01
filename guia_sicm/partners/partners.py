
# -*- coding: utf-8 -*-

from re import A
from odoo import models, fields, api


class codsicm(models.Model):
    _inherit= 'res.partner'

    codsicm = fields.Char(string='Codigo SICM')