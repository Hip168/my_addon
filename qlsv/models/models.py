from odoo import models, fields, api

class Lop(models.Model):
    _name = 'qlsv.lop'
    _description = 'Lop Hoc'

    name = fields.Char(string='Ten Lop', required=True)
    giang_vien_id = fields.Many2one('res.users', string='Giang Vien', required=True)
    sinh_vien_ids = fields.Many2many('res.users', string='Sinh Vien')
    description = fields.Text(string='Mo Ta')

