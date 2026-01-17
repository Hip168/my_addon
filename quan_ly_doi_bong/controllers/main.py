# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class FootballController(http.Controller):

    # Route WITH CORS enabled
    @http.route(
        "/football/players",
        type="json",
        auth="public",
        cors="*",
        methods=["POST", "OPTIONS"],
    )
    def get_players(self):
        players = request.env["football.player"].sudo().search([])
        return {
            "status": "success",
            "data": [
                {"id": p.id, "name": p.name, "position": p.position} for p in players
            ],
        }

    # Route WITHOUT explicit CORS (default Odoo behavior usually denies cross-origin unless configured)
    @http.route("/football/teams", type="json", auth="public", methods=["POST"])
    def get_teams(self):
        teams = request.env["football.team"].sudo().search([])
        return {
            "status": "success",
            "data": [{"id": t.id, "name": t.name} for t in teams],
        }
