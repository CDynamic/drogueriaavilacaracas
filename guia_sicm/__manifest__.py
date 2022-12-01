# -*- coding: utf-8 -*-
{
    'name': "Modulo para Control de Medicamentos Venezuela",

    'summary': """
        Modulo para Control de Medicamentos""",

    'description': """
       Modulo para  La Guía Única de Movilización, Seguimiento y Control de Medicamentos (SICM) 
       tiene como fin controlar y hacer seguimiento , los inventarios y la recepción y de comercialización o distribución de medicamentos y otros productos farmacéuticos registrados.
    """,

    'author': "Conceptual Dynamic",
    'website': "https://conceptualdynamic.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account', 'contacts','sale','stock'],
    'external_dependencies': {
        'python': ['pdfkit',],
        },
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'credentials/credentials.xml',
        'accounts/accounts.xml',      
        'automation/automation.xml',
        'guidesMobilization/guidesMobilization.xml',
        'itemsGuidesMobilization/itemsGuidesMobilization.xml',
        'partners/partners.xml',
        'inventory/inventory.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
