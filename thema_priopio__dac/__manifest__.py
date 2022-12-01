# -*- coding: utf-8 -*-
{
    'name': "Theme DAC Enterprise",

    'summary': """este tema tienen la finalidad mostrar a un cliente la apariencia """,
    'description': """tema adaptado para la DAC""",
    "category": "Themes/Backend",
    "version": "DAC.0.0.1",
    'author': 'conceptualdynamic',
    'company': 'conceptual dynamic',
    'maintainer': 'conceptual dynamic',
    'website': "https://conceptualdynamic.com",
    "depends": ['base', 'web_enterprise', 'web'],
    "data": [
        'views/icons.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            "thema_priopio__dac/static/src/scss/theme_accent.scss",
            "thema_priopio__dac/static/src/scss/navigation_bar.scss",
            "thema_priopio__dac/static/src/scss/datetimepicker.scss",
            "thema_priopio__dac/static/src/scss/theme.scss",
            "thema_priopio__dac/static/src/scss/sidebar.scss",
            "thema_priopio__dac/static/src/js/chrome/sidebar.js",
            "thema_priopio__dac/static/src/js/fields/basic_fields.js",
            "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&amp;display=swap",
        ],

        'web.assets_qweb': [
            'thema_priopio__dac/static/src/xml/top_bar.xml',
            'thema_priopio__dac/static/src/xml/sidebar.xml',
        ],
        'web.assets_frontend': [
            "thema_priopio__dac/static/src/scss/login.scss",
            "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&amp;display=swap",
        ],
    },
    'license': 'LGPL-3',
    'pre_init_hook': 'test_pre_init_hook',
    'post_init_hook': 'test_post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
