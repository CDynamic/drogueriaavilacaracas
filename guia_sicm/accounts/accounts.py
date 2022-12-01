from operator import invert
from odoo import models, fields, api



class guíasMovilización(models.Model):
    _inherit = 'account.move'

    generarGuia = fields.Boolean(string='Guia de Movilizacion', readonly=False)
    guiacreadad = fields.Boolean(string='Bandera', readonly=False)
    guia_id = fields.Many2one(comodel_name='guia_sicm.guias',inverse_name='id',domain="[('status','=','1')]" ,string='Guias')
