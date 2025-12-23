{
    "name": "zoo",
    "author": "hip",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["base"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/dashboard_action.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "zoo/static/src/dashboard/**/*",
        ],
    },
}
