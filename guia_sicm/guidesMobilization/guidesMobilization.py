
import pdfkit
import os
import base64
from odoo.tools.misc import find_in_path

from odoo import models, fields, api ,_
from odoo.modules import get_module_resource

from odoo.exceptions import UserError
from suds.client import Client
from os import remove

from odoo.exceptions import UserError
import gettext
from suds.client import Client



class guidesMobilization(models.Model):
    _name = 'guia_sicm.guias' 
    _description = 'Guias'

    name = fields.Char(default='')
    cliente = fields.Many2one( comodel_name='res.partner',string='Cliente',required=True)
    factura = fields.Many2many( comodel_name='account.move', relation='guides_document_rel', string='Factura',required=True)
    invoice_origin = fields.Many2many(comodel_name='sale.order', relation='guides_order_rel', string='ordenes',required=False)
    guia = fields.Integer(string='N° de Guía')
    pdf_guia = fields.Binary(string='Guia Pdf')
    bultos = fields.Integer(string='Bultos')
    type = fields.Selection([('A', 'Automatica'),('M', 'Manual')], string='Tipo De Carga', default='M') 
    status = fields.Selection([('1', 'Procesando'),('2', 'Abierta'),('3','Aprobada'),('4','Anulada'),('5','Recibida'),('6','Anulada Guia pendiente'),('7','Pendiente por Stock'),('9','Procesando por Stock')],default='1',string='Estatus de la guia')
    backorder_id = fields.Integer(string='backorder_id',required=False)

    def detalle_items(self):
        view_id = self.env.ref('guia_sicm.view_itemsguia_visit').id
        ids=[]
        const = self.env['guia_sicm.iguias'].search([('guides', '=', self.id)])
        for i in const:
            ids.append(i.id)
        context = self._context.copy()
        return {
            'name':'Items de la factura',
            # 'view_type':'form',
            'view_mode':'tree,form',
            "views": [[False, "tree"], [False, "form"]],
            'res_model':'guia_sicm.iguias',
            'view_id':False,
            'type':'ir.actions.act_window',
            
            'target':'new',
            # 'context':context,
            'domain': [('id','in',ids)],
        }

    # @api.model
    def crear_guia(self):
        config = pdfkit.configuration(wkhtmltopdf= find_in_path('wkhtmltopdf'))
        if self.status == '1' or self.status == '6' or self.status == '9':
            url = "http://www.sicm.gob.ve/sicm.php?wsdl"
            url_guia='http://www.sicm.gob.ve/g_4cguia.php?id_guia='
            cli= Client(url)
            credentials=self.env['guia_sicm.credentials'].search([('estatus', '=', True)])
            if credentials.code_segurity == False:
                raise UserError('Por favor validar las credenciales Las mismas deben estar activas')
            if self.bultos <= 0:
                return {
                    'name': _('Agregar Bultos'),
                    'view_mode': 'form',
                    'res_model': 'guia_sicm.guias',
                    'view_id': self.env.ref('guia_sicm.view_guias_Movilizacion_view_Bultos').id,
                    'type': 'ir.actions.act_window',
                    'res_id': self.id,
                    'context': {'default_order_id': self.id},
                    'target': 'new'
                }

            if self.cliente.codsicm == False :
                raise UserError('cliente no posee codigo SICM')
        
            if self.invoice_origin:
                
                for so in self.invoice_origin:
                    stock = self.env['stock.picking'].search([('origin', '=',so.name)])
                    
                    if stock.state != 'done':
                        raise UserError('la orden '+ so.name +' no se encuentra confirmada su Entrega')


            documento= ''
            for i in self.factura:  
                documento += i.name.split('/')[2]+','

            inicializar_guia = cli.service.inicializar_guia(str(credentials.code_segurity), str(self.cliente.codsicm) , str(self.bultos),documento )
            validate = inicializar_guia.split(';')           
            if validate[0] == '0':
                raise UserError(validate[1]+'Las credenciales o Código SICM no coinciden, por favor confirme o comuníquese con el equipo de soporte.')
            
            pdf = pdfkit.from_url(url_guia+str(inicializar_guia),  str(inicializar_guia)+'.pdf',configuration=config)
            with open( str(inicializar_guia)+'.pdf', "rb") as pdf_file:
                encoded_string = base64.b64encode(pdf_file.read())   

            remove( str(inicializar_guia)+'.pdf')
            self.write({'status': '2','guia':inicializar_guia,'pdf_guia':encoded_string})
            const = self.env['guia_sicm.iguias'].search([('guides', 'in', self.id),('status','=','0')])
            for i in const:
                lote= i.lote
                productos = cli.service.getproducto(credentials.code_segurity, i.Product.barcode)
                if productos != 'NE':
                    guia_detalle = cli.service.guia_detalle(str(credentials.code_segurity), inicializar_guia, i.Product.barcode, lote, i.price, i.quantity)
                
                else:
                    guia_detalle = cli.service.guia_detalle_desc(str(credentials.code_segurity), inicializar_guia, i.Product.barcode, lote, i.price, i.quantity,i.Product.name)
            
            pdf = pdfkit.from_url(url_guia+str(inicializar_guia),  str(inicializar_guia)+'.pdf',configuration=config)
            with open( str(inicializar_guia)+'.pdf', "rb") as pdf_file:
                encoded_string = base64.b64encode(pdf_file.read())   

            remove( str(inicializar_guia)+'.pdf')
            self.write({'status': '2','guia':inicializar_guia,'pdf_guia':encoded_string})
            

                

    def aprobar_guia(self):
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        url = "http://www.sicm.gob.ve/sicm.php?wsdl"
        url_guia='http://www.sicm.gob.ve/g_4cguia.php?id_guia='
        cli= Client(url)
        credentials=self.env['guia_sicm.credentials'].search([('estatus', '=', True)])
        if credentials.code_segurity == False:
            raise UserError('Por favor validar las credenciales Las mismas deben estar activas')
#        Aprobar Guía:guia_validar(cod_seguridad, cod_guia)
#        Parámetros de Entrada: cod_seguridad, cod_guia
#        Retorna: Si es correcto el Numero de Guía Aprobada, en caso de Error el valor 0.
        guia_validar = cli.service.guia_validar(str(credentials.code_segurity), str(self.guia))
            
        if guia_validar != '0':
            pdf = pdfkit.from_url(url_guia+str(self.guia), str(self.guia)+'.pdf',configuration=config)
            with open(str(self.guia)+'.pdf', "rb") as pdf_file:
                encoded_string = base64.b64encode(pdf_file.read())   

            remove(str(self.guia)+'.pdf')
            self.write({'status': '3','pdf_guia':encoded_string})
            const = self.env['guia_sicm.iguias'].search([('guides', 'in', self.id),('status','=','0')])
        

    def write(self, vals):
        for fact in self.factura:
            if fact.guiacreadad == False:
                Items = self.env['account.move.line'].search([('move_id', '=', fact.name),('product_id','!=',False)])
                for i in Items:
                    if self._origin.cliente.id != i.partner_id.id:
                        raise UserError('No se puede agregar la factura Nro:'+ fact.name +'El cliente de la guia no se encuentra asignado')
                        
                    if gtest:
                        itemsGuia=  {
                            'guides':self._origin,
                            'Product': i.product_id.id,
                            'price': i.price_unit,
                            'quantity': i.quantity,
                            'status': '0',
                            
                        }
                        itemsGuiaInsert = self.env['guia_sicm.iguias'].create(itemsGuia)
                fact.write({'guiacreadad': True,})
                
            else:
                if 'factura' in vals:
                    raise UserError('No se puede agregar la factura Nro:'+ fact.name +'ya se encuentra asignada a otra guia')
                
        super(guidesMobilization, self).write(vals)
        
        


    @api.onchange('factura')
    def funcionAgregaritems(self,context=None):
        for fact in self.factura:
            if fact.guiacreadad == False:
                Items = self.env['account.move.line'].search([('move_id', '=', fact.name),('product_id','!=',False)])
                
                for i in Items:
                    if self._origin.cliente.id != i.partner_id.id:
                        return {
                            'warning': {
                                'title': 'Error al agregar  ',
                                'message': 'No se puede agregar la factura Nro:'+ fact.name +' El cliente de la guia no se encuentra asignado' }
                                }
            else:
                
                return {
                'warning': {
                    'title': 'Error al agregar  ',
                    'message': 'No se puede agregar la factura Nro:'+ fact.name +' ya se encuentra asignada a otra guia' }
            }

    def anular_guia(self):
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        if self.guia==False:
            self.write({"status":"4","pdf_guia":''})
            title = "Anulacion!"
            message = "Guia Anulada!"
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'sticky': True,
                    }
            } 

        url = "http://www.sicm.gob.ve/sicm.php?wsdl"
        url_guia='http://www.sicm.gob.ve/g_4cguia.php?id_guia='
        cli= Client(url)

        credentials=self.env['guia_sicm.credentials'].search([('estatus', '=', True)])
        stGuia= cli.service.guia_status(credentials.code_segurity, self.guia)
        if stGuia != '0' :
            if stGuia.split(';')[2]!='APR':
                anular = cli.service.guia_anular(credentials.code_segurity, self.guia)
                if anular != '0':
                    pdf = pdfkit.from_url(url_guia+str(self.guia), str(self.guia)+'.pdf',configuration=config)
                    with open(str(self.guia)+'.pdf', "rb") as pdf_file:
                        encoded_string = base64.b64encode(pdf_file.read())   

                    remove(str(self.guia)+'.pdf')
                    self.write({'status': '4','pdf_guia':encoded_string})

                    title = "Anulacion!"
                    message = "Guia "+ str(self.guia) +"Anulada!"
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': title,
                            'message': message,
                            'sticky': False,
                            }
                    } 
            else:
                raise UserError('no se puede anular la guia')
        else:
            self.write({"status":"4"})
            title = "Anulacion!"
            message = "Guia Anulada!"
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'sticky': False,
                    }
            }  
    def guardar_bultos(self):
        pass  

   