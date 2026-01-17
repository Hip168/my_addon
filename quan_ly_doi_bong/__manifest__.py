# -*- coding: utf-8 -*-
{
    "name": "Quản Lý Đội Bóng",
    "summary": """
        Quản lý cầu thủ, đội bóng và các trận đấu.
        Thực nghiệm CORS và Many2many intermediary.
    """,
    "description": """
        Module quản lý đội bóng bao gồm:
        - Quản lý Cầu thủ (Player)
        - Quản lý Đội bóng (Team)
        - Quản lý Trận đấu (Match)
        - Chi tiết trận đấu (Lineup/Performance) - Many2many with fields
        - API Test CORS
    """,
    "category": "Sports",
    "version": "0.1",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "reports/football_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "quan_ly_doi_bong/static/src/components/football_dashboard.js",
            "quan_ly_doi_bong/static/src/components/football_dashboard.xml",
        ],
    },
    "application": True,
}
