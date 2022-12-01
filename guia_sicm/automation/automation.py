from re import A
from suds.client import Client
from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit ='account.move'

    def action_post(self):
        rec = super().action_post()
        const=self
        # guia_id=self.env['guia_sicm.guias'].search([],order='id asc')[-1].id
        
                        
        if const.generarGuia and const.name != '/' and const.guiacreadad == False:
            guiaGenerateDict = {
                'name': 'Guia/'+str(const.id+1),
                'factura': const,
                'cliente':const.partner_id.id,
                'bultos':0,
                'type':'A',
                'status':'1',
            }
            if const.invoice_origin:
                guiaGenerateDict['invoice_origin']=self.env['sale.order'].search([('name', '=', const.invoice_origin)])
            if const.guia_id:
                guiaGenerate2 = self.env['guia_sicm.guias'].search([('id', '=', const.guia_id.id)])
                if guiaGenerate2.cliente.id != const.partner_id.id:
                    
                    guiaGenerate = self.env['guia_sicm.guias'].create(guiaGenerateDict)
                    const.write({'guia_id': guiaGenerate.id,})
                else:
                    guiaGenerate =guiaGenerate2
                    
                    self.env.cr.execute("INSERT INTO guides_document_rel (guia_sicm_guias_id,account_move_id) VALUES ('%s','%s')" %(const.guia_id.id,f_ids))
                    if const.invoice_origin:
                        
                        self.env.cr.execute("INSERT INTO guides_order_rel (guia_sicm_guias_id,sale_order_id) VALUES ('%s','%s')" %(const.guia_id.id,self.env['sale.order'].search([('name', '=', const.invoice_origin)]).id))    
            else:
                
                guiaGenerate = self.env['guia_sicm.guias'].create(guiaGenerateDict)
                const.write({'guia_id': guiaGenerate.id,})
                
            if guiaGenerate != 0:

                Items = self.env['stock.move'].search([('origin', '=',const.invoice_origin)])
                
            for i in Items:
                ItemsStock = self.env['stock.move.line'].search([('move_id', '=', i.id)])
                
                for istock in ItemsStock:
                    
                    if istock.product_qty>0:
                        quantity=istock.product_qty
                    elif istock.product_uom_qty>0:
                        quantity=istock.product_uom_qty
                    else:
                        quantity=istock.qty_done
                    itemsGuia=  {
                        'guides':guiaGenerate,
                        'Product': i.product_id.id,
                        'price': i.sale_line_id.price_unit,
                        'quantity': quantity,
                        'lote': istock.lot_id.name,
                        'status': '0',    
                    }
                    if const.invoice_origin:
                        itemsGuia['invoice_origin']=const.invoice_origin
                    itemsGuiaInsert = self.env['guia_sicm.iguias'].create(itemsGuia)

                const.write({'guiacreadad': True,})
                insertInventary= self.env['stock.picking'].search([('origin', '=', const.invoice_origin)]).write({'guias': guiaGenerate})
        return rec
    
        
    
    @api.model
    def revision_due_invoices(self,context=None):
        f_ids=self.env['account.move'].search([],order='id asc')[-1].id
        const = self.env['account.move'].search([('id', '=', f_ids)])
        createg =False
        if const.generarGuia and const.name != '/' and const.guiacreadad == False:
            guiaGenerateDict = {
                'name': 'Guia/'+str(f_ids+1),
                'factura': const,
                'cliente':const.partner_id.id,
                'bultos':0,
                'type':'A',
                'status':'1',
            }
            if const.invoice_origin:
                guiaGenerateDict['invoice_origin']=self.env['sale.order'].search([('name', '=', const.invoice_origin)])
            if const.guia_id:
                guiaGenerate2 = self.env['guia_sicm.guias'].search([('id', '=', const.guia_id.id)])
                if guiaGenerate2.cliente.id != const.partner_id.id:
                    guiaGenerate = self.env['guia_sicm.guias'].create(guiaGenerateDict)
                    const.write({'guia_id': guiaGenerate.id,})
                else:
                    guiaGenerate =guiaGenerate2

                    self.env.cr.execute("INSERT INTO guides_document_rel (guia_sicm_guias_id,account_move_id) VALUES ('%s','%s')" %(const.guia_id.id,f_ids))
                    if const.invoice_origin:
                        self.env.cr.execute("INSERT INTO guides_order_rel (guia_sicm_guias_id,sale_order_id) VALUES ('%s','%s')" %(const.guia_id.id,self.env['sale.order'].search([('name', '=', const.invoice_origin)]).id))    
            else:
                guiaGenerate = self.env['guia_sicm.guias'].create(guiaGenerateDict)
                const.write({'guia_id': guiaGenerate.id,})
                
            if guiaGenerate != 0:

                Items = self.env['stock.move'].search([('origin', '=',const.invoice_origin)])
                
            for i in Items:
                ItemsStock = self.env['stock.move.line'].search([('move_id', '=', i.id)])
                
                for istock in ItemsStock:
                    print(ItemsStock)
                    if istock.product_qty>0:
                        quantity=istock.product_qty
                    elif istock.product_uom_qty>0:
                        quantity=istock.product_uom_qty
                    else:
                        quantity=istock.qty_done
                    itemsGuia=  {
                        'guides':guiaGenerate,
                        'Product': i.product_id.id,
                        'price': i.sale_line_id.price_unit,
                        'quantity': quantity,
                        'lote': istock.lot_id.name,
                        'status': '0',    
                    }
                    if const.invoice_origin:
                        itemsGuia['invoice_origin']=const.invoice_origin
                    itemsGuiaInsert = self.env['guia_sicm.iguias'].create(itemsGuia)

                const.write({'guiacreadad': True,})
                insertInventary= self.env['stock.picking'].search([('origin', '=', const.invoice_origin)]).write({'guias': guiaGenerate})

    
    

       
