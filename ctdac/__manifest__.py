# -*- coding: utf-8 -*-
{
    'name': "ctdac",

    'summary': """
        modulo como complemento del thema DAC""",

    'description': """
        odulo como complemento del thema DAC
    """,
    'author': 'conceptual dynamic Techno Solutions',
    'company': 'conceptual dynamic Techno Solutions',
    'maintainer': 'conceptual dynamic Techno Solutions',
    'website': "https://www.conceptualdynamic.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    'assets': {
        'web.assets_frontend': [
            'ctdac/static/src/css/**/*',
            'ctdac/static/src/lib/leaflet',
            'ctdac/static/src/**/*',
            
        ],
    },

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
