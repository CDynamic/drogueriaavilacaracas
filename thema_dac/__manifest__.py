
{
    'name': 'Theme Dac',
    'description': 'Theme Dac is an attractive and modern eCommerce Website theme',
    'summary': 'Design Web Pages with theme Dac',
    'category': 'Theme/eCommerce',
    'version': '15.0.1.0.0',
    'author': 'conceptual dynamic Techno Solutions',
    'company': 'conceptual dynamic Techno Solutions',
    'maintainer': 'conceptual dynamic Techno Solutions',
    'website': "https://www.conceptualdynamic.com",
    'depends': ['website','territorial_pd','ctdac'],
    'data': [
        
        'views/views.xml',
        'views/header.xml',
        'views/footer.xml',
        'views/view_Back.xml',
        'views/map_cliente.xml',
        'views/map_aliado.xml',
        'views/snippets/banner.xml',
        
    ],
    'images': [
    ],

    'assets': {
        'web.assets_frontend': [
            'thema_dac/static/src/js/front/thema_main.js',
        ],
        'web.assets_backend': [
            "thema_dac/static/src/css/back_style.css",
            "thema_dac/static/src/js/lib/leaflet.js",
            "thema_dac/static/src/js/back_main.js",
            
        ],
        
    },

    'installable': True,
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}
