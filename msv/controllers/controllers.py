# from odoo import http


# class /users/leminhdao168/documents/career/odoo/odooLocal19/my-addon/msv(http.Controller):
#     @http.route('//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv.listing', {
#             'root': '//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv',
#             'objects': http.request.env['/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv./users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv'].search([]),
#         })

#     @http.route('//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv//users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv/objects/<model("/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv./users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/users/leminhdao168/documents/career/odoo/odoo_local_19/my-addon/msv.object', {
#             'object': obj
#         })

