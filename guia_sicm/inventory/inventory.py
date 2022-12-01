# from odoo import models, fields, api
import pdfkit
import os
import base64
from odoo import api, fields, models, SUPERUSER_ID, tools,  _
from odoo.exceptions import UserError
from suds.client import Client
from odoo.modules import get_module_resource
from os import remove

class inventoryAdd(models.Model):
    _inherit = 'stock.picking'

    guias = fields.Many2many(comodel_name='guia_sicm.guias',domain="[('status','=','1')]" ,string='Guias')
    

    def action_set_quantities_to_reservation(self):
        res =  super().action_set_quantities_to_reservation()
        if self.guias.backorder_id and len(self.guias.ids) > 0:
            
            for i in self:
                guia = i.guias
                if guia.status == '7':
                    Items = self.env['stock.move'].search([('origin', '=',i.origin),('picking_id','=',guia.backorder_id)])
                    guia.write({'status': '9',})
                    for it in Items:
                        ItemsStock = self.env['stock.move.line'].search([('move_id', '=', it.id),('picking_id','=',guia.backorder_id)])
                        for istock in ItemsStock:
                            if istock.product_qty>0:
                                quantity=istock.product_qty
                            elif istock.product_uom_qty>0:
                                quantity=istock.product_uom_qty
                            else:
                                quantity=istock.qty_done
                            itemsGuia=  {
                                'guides':guia,
                                'Product': istock.product_id.id,
                                'price': it.sale_line_id.price_unit,
                                'quantity': quantity,
                                'lote': istock.lot_id.name,
                                'status': '0',    

                            }
                            if i.origin:
                                itemsGuia['invoice_origin']=i.origin
                            itemsGuiaInsert = self.env['guia_sicm.iguias'].create(itemsGuia)
                        
             
        return res

    
    
        

class productBarcode(models.Model):
    _inherit = 'product.template'


    @api.onchange('barcode')
    def guardarBultos(self,context=None):
        url = "http://www.sicm.gob.ve/sicm.php?wsdl"
        credentials=self.env['guia_sicm.credentials'].search([('estatus', '=', True)])
        cliente= Client(url)
        if self.barcode:
            if self._origin.barcode != self.barcode:
                productos = cliente.service.getproducto(credentials.code_segurity, self.barcode)
                if productos =='NE':
                    return {
                    'warning': {
                    'title': 'Alerta',
                    'message': 'El codigo de barra No pertenece a un producto registrado SICM se debera registrar el mismo' }
                    }
            
                self.write({'name': productos})

class SaleOrderCancelGuiade(models.TransientModel):
    _name = 'sale.order.cancel.guia'
    _description = "Sales Order Cancel Guiade"

    order_id = fields.Many2one('sale.order', string='Sale Order guiade', required=True, ondelete='cascade')
    

    def action_cancel_guia(self):
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        guiaObj = self.env['guia_sicm.guias'].search([('invoice_origin' ,'=',self.order_id.id)])
        if guiaObj.exists():
            
            if guiaObj.guia > 0: 
                url = "http://www.sicm.gob.ve/sicm.php?wsdl"
                url_guia='http://www.sicm.gob.ve/g_4cguia.php?id_guia='
                cli= Client(url)
                credentials=self.env['guia_sicm.credentials'].search([('estatus', '=', True)])
                if credentials.exists():
                    stGuia= cli.service.guia_status(credentials.code_segurity, guiaObj.guia)
                    if stGuia != '0' :
                        if stGuia.split(';')[2]!='APR':
                            anular = cli.service.guia_anular(credentials.code_segurity, guiaObj.guia)
                            if anular != '0':
                                img_path = get_module_resource('guia_sicm','static','tmp')
                                
                                pdf = pdfkit.from_url(url_guia+str(guiaObj.guia),  str(guiaObj.guia)+'.pdf',configuration=config)
                                with open( str(guiaObj.guia)+'.pdf', "rb") as pdf_file:
                                    encoded_string = base64.b64encode(pdf_file.read())   

                                remove( str(guiaObj.guia)+'.pdf')
                                itemsGuia =self.env['guia_sicm.iguias'].search([('guides','=',guiaObj.id),('invoice_origin','=',self.order_id.name)])
                                if itemsGuia.exists():
                                    for items in itemsGuia:
                                        items.write({'status': '2'})

                                for guiadoc in guiaObj.factura:
                                    if guiadoc.invoice_origin == self.order_id.name:
                                        self.env.cr.execute("delete from guides_document_rel where account_move_id = '%s' and guia_sicm_guias_id = '%s';" %(guiadoc.id,guiaObj.id))
                                    
                                guiaObj.write({'status': '6','pdf_guia':encoded_string})
                                # return super(saleOrder, self).action_cancel()
                                return self.order_id.with_context({'disable_cancel_warning': False}).action_cancel()
                                
                        else:
                            raise UserError('no se puede anular la guia')
                else:
                    raise UserError('no se puede anular la guia error en las credenciales ')
            else:
                for guiadoc in guiaObj.factura:
                    if guiadoc.invoice_origin == self.order_id.name:
                        self.env.cr.execute("delete from guides_document_rel where account_move_id = '%s' and guia_sicm_guias_id = '%s';" %(guiadoc.id,guiaObj.id))
                guiaObj.write({'status': '6'})
                                # return super(saleOrder, self).action_cancel()
                return self.order_id.with_context({'disable_cancel_warning': False}).action_cancel()

class saleOrder(models.Model):
    _inherit = 'sale.order'

    def action_cancel(self):
        guiaObj = self.env['guia_sicm.guias'].search([('invoice_origin' ,'=',self.id),('status','in',['1','2'])])
        if guiaObj.exists():
            return {
                    'name': _('Alert order with guide '),
                    'view_mode': 'form',
                    'res_model': 'sale.order.cancel.guia',
                    'view_id': self.env.ref('guia_sicm.view_guias_Movilizacion_view_inventary2').id,
                    'type': 'ir.actions.act_window',
                    'context': {'default_order_id': self.id},
                    'target': 'new'
                }
        else:
            return super(saleOrder, self).action_cancel()

class StockBackorderConfirmationGuia(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self): 
        res = super().process()
        if res == True:
            pickings_to_do = self.env['stock.picking']
            for line in self.backorder_confirmation_line_ids:
                if line.to_backorder is True:
                    pickings_to_do |= line.picking_id
               
            for pickings_to_do_items in pickings_to_do:
                cpnsulta = self.env['stock.picking'].search([('backorder_id','=',pickings_to_do_items.id)])
                if cpnsulta.origin:
                    move = self.env['account.move'].search([('invoice_origin', '=', cpnsulta.origin)])   
                      
                    guia_id=self.env['guia_sicm.guias'].search([],order='id asc')[-1].id
                    guiaGenerateDict = {
                            'name': 'Guia/'+str(guia_id+1),
                            'factura': move,
                            'cliente':move.partner_id.id,
                            'bultos':0,
                            'type':'A',
                            'status':'7',
                            'backorder_id': cpnsulta.id,
                            'invoice_origin':self.env['sale.order'].search([('name', '=', pickings_to_do_items.origin)])
                        }
                    guiaGenerate = self.env['guia_sicm.guias'].create(guiaGenerateDict)

                    if guiaGenerate != 0:
                        insertInventary= cpnsulta.write({'guias': guiaGenerate})
        return res



    