
from odoo import api, fields, models, SUPERUSER_ID, tools,  _



class WebCategory(models.Model):
    _name = 'thema_dac.category'
    _description = 'WebCategory'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    status  = fields.Boolean(string='Estatus')

class productPublished(models.Model):
    _inherit =  'product.template'
    Published  = fields.Boolean(string='Publicado en la WEB')

class productCategory(models.Model):
    _inherit =  'product.category'
    status  = fields.Boolean(string=' Activo Para la WEB')

class clientCategorys(models.Model):
    _inherit= 'res.partner'
    
    
    status  = fields.Boolean(string=' Activo Para la WEB')
    types = fields.Selection([('A', 'Aliado'), ('C', 'Cliente')], string='Tipo', required=False)
    website_leaflet_lat = fields.Char('latitude', required=False)
    website_leaflet_lng = fields.Char('longitude',  required=False)
    hors = fields.Char(string='Horario')


class WebSubCategory(models.Model):
    _name = 'thema_dac.sub_category'

    _description = 'WebSubCategory'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    status  = fields.Boolean(string='Estatus')
    category = fields.Many2one(string='Categoria Padre', 
    comodel_name='thema_dac.category',
    )

class WebContacts(models.Model):
    _name = 'thema_dac.contacts'
    _description = 'WebContacts'

    name = fields.Char(string='Nombre')
    hors = fields.Char(string='Horario')
    description = fields.Char(string='Descripción')
    country_id = fields.Many2one(
        'res.country',
        string=u'País',
        ondelete='restrict',
        help=u"País",
        default=lambda self: self.env['res.country'].search(
            [('name', '=', 'Venezuela')]
        )[0].id
    )
    state_id = fields.Many2one(
        "res.country.state",
        string='Estado',
        ondelete='restrict',
        help=u"Estado"
    )
    municipality_id = fields.Many2one(
        "res.country.state.municipality",
        string="Municipio",
        domain="[('state_id', '=', state_id)]",
        ondelete='restrict',
        help=u"Municipio"
    )
    parish_id = fields.Many2one(
        "res.country.state.municipality.parish",
        string="Parroquia",
        ondelete='restrict',
        domain="[('municipality_id', '=', municipality_id)]",
        help=u"Parroquia"
    )
    date = fields.Datetime(string='Fecha')
    status  = fields.Boolean(string='Estatus')
    type = fields.Selection([('A', 'Aliado'), ('C', 'Cliente')], string='Tipo', required=True)
    domcument_type = fields.Selection([('N', 'Natural'), ('J', 'Juridico')], string='Tipo', required=True)
    image = fields.Binary(string='Logo')
    website_leaflet_lat = fields.Float('Coord latitude')
    website_leaflet_lng = fields.Float('Coord longitude')
    website_leaflet_enable = fields.Boolean("Enable/Disable leaflet")
    # website_leaflet_size = fields.Integer("Size of map(230 - norm)")



class WebProducts(models.Model):
    _name = 'thema_dac.products'
    _description = 'products'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripción')
    date = fields.Datetime(string='Fecha')
    category = fields.Many2one(string='Categoria', comodel_name='thema_dac.category')
    category_sub = fields.Many2one(
        "thema_dac.sub_category",
        string="Sub Categoria",
        domain="[('category', '=', category)]",
        ondelete='restrict',
        help=u"Sub Categoria"
    )
    status  = fields.Boolean(string='Estatus', )
    Published  = fields.Boolean(string='Publicado en la WEB')
    image = fields.Binary(string='Imagen')

# class View(models.Model):
#     _inherit = 'ir.ui.view'

#     type = fields.Selection(selection_add=[('map', "Map")])

# class ActWindowView(models.Model):
#     _inherit = 'ir.actions.act_window.view'

#     view_mode = fields.Selection(selection_add=[('map', "Map")])

# class WebBanner(models.Model):
#     _name = 'thema_dac.banner'
#     _description = 'Banner'

#     name = fields.Char(string='Nombre')
#     description = fields.Char(string='Descripción')
#     page_menu = fields.Many2one(string='Categoria', comodel_name='website.menu')
#     date = fields.Datetime(string='Fecha')
#     category = fields.Many2one(string='Categoria', comodel_name='thema_dac.category')
#     category_sub = fields.Many2one(
#         "thema_dac.sub_category",
#         string="Sub Categoria",
#         domain="[('category', '=', category)]",
#         ondelete='restrict',
#         help=u"Sub Categoria"
#     )
#     status  = fields.Boolean(string='Estatus', )
#     Published  = fields.Boolean(string='Publicado en la WEB')
#     image = fields.Binary(string='Imagen')