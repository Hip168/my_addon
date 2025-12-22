from odoo import models, fields, api

class TestDecoration(models.Model):
    _name = "test.decoration"
    _description = "Test Decoration"

    name = fields.Char(string="Name",)
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Sex",)
    day_of_birth = fields.Date(string="Day of Birth",)
    type_sex = fields.Char(string="Type Sex", compute='_compute_type_sex')
    @api.depends('sex')
    def _compute_type_sex(self):
        for record in self:
            record.type_sex = '1' if record.sex == 'male' else '0'

    def action_test_api_model(self):
        """
        Đây là hàm được gọi từ nút bấm (Button).
        Nó là cầu nối để gọi hàm @api.model bên dưới.
        """
        # Gọi hàm @api.model thông qua self.env
        self.env['test.decoration'].check_and_fill_dob()
        
        # Reload lại giao diện để thấy dữ liệu mới
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    @api.model
    def check_and_fill_dob(self):
        records_to_update = self.search([('day_of_birth', '=', False), ('sex', '=', 'male')])
        if records_to_update:
            records_to_update.write({
                'day_of_birth': fields.Date.today(),
                'type_sex': '1',
            })