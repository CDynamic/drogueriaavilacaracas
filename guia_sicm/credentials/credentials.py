from odoo import models, fields, api




class modelCMCredentials(models.Model):
    _name = 'guia_sicm.credentials'

    code_sicm = fields.Char(string='Código SICM')
    code_segurity= fields.Char(string='Código Seguridad')   
    estatus = fields.Boolean(string='Estatus', readonly=False)

    def toggle_state(self):
        credentials = self.env['guia_sicm.credentials'].search([('estatus','=',True)])
        if credentials.exists():
            credentials.update({'estatus': False})
        self.estatus = not self.estatus

        
