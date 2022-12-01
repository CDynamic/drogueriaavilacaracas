# -*- coding: utf-8 -*-
from posixpath import supports_unicode_filenames
import re
from unicodedata import category
from odoo import http
from odoo.http import request, Response
import json



    
class SnoppetController(http.Controller):
    


    @http.route('/get_main_product', auth="public", method=['GET'], csrf=False , website=True)
    def get_main_product(self):
        try:
            print('category')
            main_products = request.env['product.template'].sudo().search([('Published', '=', True)], order='create_date asc', limit=8)
            category = request.env['product.category'].sudo().search([('parent_id','=',False),('status', '=', True)], order='name asc')
            # print(category)
            sub_category = request.env['product.category'].sudo().search([('parent_id','!=',False),('status', '=', True)], order='name asc')
            
            # print(sub_category)
            values = {
                'ids_t':False,
                "dor":False,
                'main_products': main_products,
                'main_category': category,
                'main_sub_category': sub_category,    

            }
            
            response = http.Response(template='thema_dac.galeriaseisProductos_snipet', qcontext=values)
            return response.render()
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)


    @http.route('/get_main_product/<model("product.category"):obj>',  type='http', auth="public", website=True, sitemap=False)
    # @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=False)
    def object(self, obj, **kw):
        print(obj)
        try:
            main_products = request.env['product.template'].sudo().search([('Published', '=', True),('categ_id', '=', int(obj.id) )], order='id asc', limit=8)
            print(main_products)
            # main_products = request.env['product.template'].sudo().search([('Published', '=', True)], limit=8)
            category = request.env['product.category'].sudo().search([('parent_id','=',False),('status', '=', True)], order='name asc')
            sub_category = request.env['product.category'].sudo().search([('parent_id','!=',False),('status', '=', True)], order='name asc')
            values = {
                'ids_t':obj.id,
                "dor": obj.id,
                'main_products': main_products,
                'main_category': category,
                'main_sub_category': sub_category,
                

            }
            
            response = http.Response(template='thema_dac.galeriaseisProductos_snipet', qcontext=values)
            
            return response.render()
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)


    @http.route('/get_main_cliente',  auth="public", method=['GET'], csrf=False , website=True)
    def object_get_(self):
        try:
           
            main_cliente = request.env['res.partner'].sudo().search([('status', '=', True),('types', '=','C')], order='id asc')
            print(main_cliente)
            main_estados = request.env['res.country.state'].sudo().search([('country_id','=',238)], order='name asc')
            values = {
                'main_sub_category': main_cliente,  
                'main_estados': main_estados

            }
            response = http.Response(template='thema_dac.mapCliente', qcontext=values)
            return response.render()
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)        


    @http.route('/get_main_municipality_filter/<model("res.country.state"):obj>', type='json', auth="public", website=True, sitemap=False)
   
    def object_municipiofiltrado(self,  obj, **kw):
        
        try:
            main_cliente = request.env['res.country.state.municipality'].sudo().search([('state_id','=',obj.id)], order='id asc')
            m=[]
            for items in main_cliente:
                values = {
                    'municipio': items.name,
                    'code': items.code,
                    'state_id' : items.state_id.id,
                }
                m.append(values)
            return Response(json.dumps(m), content_type='application/json;charset=utf-8', status=202)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)
    

    @http.route('/get_main_municipality', type="json", auth="public", method=['GET'], csrf=False , website=True)
   
    def object_get_municipio(self,args):
        
        try:
            st = request.env['res.country.state'].sudo().search([('id','=',str(args[0]['id']))])
            main_cliente = request.env['res.country.state.municipality'].sudo().search([('state_id','=',st.id)], order='id asc')
            m=[]
            for items in main_cliente:
                values = {
                    'id': items.id,
                    'municipio': items.name,
                    'code': items.code,
                    'state_id' : items.state_id.id,
                }
                m.append(values)
            
            return m
            
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)
   
    

    @http.route('/get_list_cliente',  type="json", auth="public", method=['GET'], csrf=False , website=True)
    def object_get_list(self,args):
        try:
            print(args[0]['id'])
            main_cliente = request.env['res.partner'].sudo().search([('status', '=', True),('types', '=','C'),('municipality_id','=',int(args[0]['id']))], order='id asc')
            print(main_cliente)
            m=[]
            for items in main_cliente:
                values = {
                    'id': items.id,
                    'name': items.name,
                    'hours': items.hors,
                    'address' : items.state_id.name +", "+ items.municipality_id.name +", "+ items.parish_id.name,
                    'imgen' : items.image_1920
                }
                m.append(values)
            print(m)
            return m
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)
            
        
    @http.route('/get_map_cliente',  type="json", auth="public", method=['GET'], csrf=False , website=True)
    def object_get_map(self,args):
        try:
            
            main_cliente = request.env['res.partner'].sudo().search([('id','=',int(args[0]['id']))], )
            
            m=[]
            for items in main_cliente:
                values = {
                    'id': items.id,
                    'lat': items.website_leaflet_lat,
                    'log': items.website_leaflet_lng,
                    
                }
                m.append(values)
            
            return m
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)




    # #########################################################################################(Aliados)###########################################################################################################
            
    @http.route('/get_main_aliado',  auth="public", method=['GET'], csrf=False , website=True)
    def object_get_Aliados(self):
        try:
           
            main_aliados = request.env['res.partner'].sudo().search([('status', '=', True),('types', '=','A')], order='id asc')
            main_estados = request.env['res.country.state'].sudo().search([('country_id','=',238)], order='name asc')
            values = {
                'main_sub_category': main_aliados,  
                'main_estados': main_estados

            }
            response = http.Response(template='thema_dac.map_Aliado_view', qcontext=values)
            return response.render()
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)



    @http.route('/get_list_aliado',  type="json", auth="public", method=['GET'], csrf=False , website=True)
    def object_get_list_Aliados(self,args):
        try:
            print(args[0]['id'])
            aliado = request.env['res.partner'].sudo().search([('status', '=', True),('types', '=','A'),('municipality_id','=',int(args[0]['id']))], order='id asc')
            
            m=[]
            for items in aliado:
                values = {
                    'id': items.id,
                    'name': items.name,
                    'hours': items.hors,
                    'address' : items.state_id.name +", "+ items.municipality_id.name +", "+ items.parish_id.name,
                    'imgen' : items.image_1920
                }
                m.append(values)
            return m
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)
            
        
    @http.route('/get_map_aliado',  type="json", auth="public", method=['GET'], csrf=False , website=True)
    def object_get_map_Aliados(self,args):
        try:
            
            main_cliente = request.env['res.partner'].sudo().search([('id','=',int(args[0]['id']))], )
            
            m=[]
            for items in main_cliente:
                values = {
                    'id': items.id,
                    'lat': items.website_leaflet_lat,
                    'log': items.website_leaflet_lng,
                    
                }
                m.append(values)
            
            return m
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=505)




    
