# -*- coding: utf-8 -*-
{
    "name": "OXP Demo App",
    "summary": """
        Demo App for GED Talk
    """,
    "description": """
        Demo App for GED Talk
    """,
    "author": "GED",
    "website": "https://www.odoo.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Tutorial",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "web"],
    "application": True,
    "installable": True,
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "oxp.assets": [
            # Include the full backend assets to ensure all Owl/QWeb engines are loaded
            ("include", "web.assets_backend"),
            # App files
            "oxp/static/src/**/*.xml",
            "oxp/static/src/**/*.js",
            "oxp/static/src/**/*.scss",
        ],
    },
    "license": "AGPL-3",
}
