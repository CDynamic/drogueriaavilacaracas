
from odoo import models, fields, api,_


class itemsGuidesMobilization(models.Model):
    _name = 'guia_sicm.iguias' 

    guides = fields.Many2many(comodel_name='guia_sicm.guias', relation='guides_items_rel',string='Numero de Guia',required=True)
    Product = fields.Many2one( comodel_name='product.product',string='Productos')
    price = fields.Float(string='Precio')
    lote = fields.Char(string=_('lot'))
    invoice_origin = fields.Char()
    quantity = fields.Float(string='Cantidad')
    items_guia = fields.Integer(string='N° de Items de la Guía')
    status = fields.Selection([('0', 'No Cargado'), ('1', 'Cargado'),('2', 'Anulado')], string='estatus', required=True) 
