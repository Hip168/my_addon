import json
from odoo import http
from odoo.http import request


class ZooAPI(http.Controller):

    @http.route(
        "/zoo/api/animals",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_animals(self):
        """Returns a list of all animals."""
        # sudo() is used to allow public access regardless of ACLs
        animals = request.env["animal.base"].sudo().search([])
        data = []
        for animal in animals:
            data.append(
                {
                    "id": animal.id,
                    "name": animal.name,
                    "species": animal.species_id.name,
                    "age": animal.age,
                    "health_status": getattr(
                        animal, "health_status", "N/A"
                    ),  # Handle extension fields gracefully
                }
            )
        return request.make_response(
            json.dumps({"status": "success", "data": data}),
            headers=[("Content-Type", "application/json")],
        )

    @http.route(
        "/zoo/api/cages",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def get_cages(self):
        """Returns a list of cages and their occupants."""
        cages = request.env["cage"].sudo().search([])
        data = []
        for cage in cages:
            occupants = []
            for animal in cage.animal_ids:
                occupants.append({"id": animal.id, "name": animal.name})

            data.append(
                {
                    "id": cage.id,
                    "name": cage.name,
                    "species_allowed": cage.species_id.name,
                    "occupants": occupants,
                }
            )
        return request.make_response(
            json.dumps({"status": "success", "data": data}),
            headers=[("Content-Type", "application/json")],
        )
