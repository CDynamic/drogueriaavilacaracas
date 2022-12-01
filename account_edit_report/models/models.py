# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_edit_report(models.Model):
    _name = 'account_edit_report.notas_pagar'
   

    numero = fields.Char(string='NNuemero de cuenta',required=True)
    banco = fields.Many2one('res.bank', string='Selecion de Bancos',required=True)
    cuenta = fields.Selection([('Ahorro', 'Ahorro'), ('Corriente', 'Corriente'),('Cuenta Verde', 'Cuenta Verde')], string='Cuentas', required=True) 
    status = fields.Boolean(default=True)
    

  

class datos_computados_convercion(models.Model):
    _inherit = 'account.move'


    usd = fields.Float(compute="_compute_usd")
    totalusd = fields.Float(compute="_compute_usd")



    def _compute_usd(self):
        uds= self.env['res.currency'].sudo().search([('name','=','USD')])
        rates=  self.env['res.currency.rate'].sudo().search([('currency_id','=',int(uds.id)),('name','=',self.invoice_date)])
        self.usd = rates.inverse_company_rate
        
        self.totalusd = round(self.amount_residual * rates.rate)
       
