# from odoo import http


# class /users/leminhdao168/documents/career/odoo/odooLocal19/my-addon/qlsv(http.Controller):
#     @http.route('//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv.listing', {
#             'root': '//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv',
#             'objects': http.request.env['/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv./users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv'].search([]),
#         })

#     @http.route('//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv/objects/<model("/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv./users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/qlsv.object', {
#             'object': obj
#         })

