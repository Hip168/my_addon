from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Thêm các trường tùy chỉnh cho app Pantry
    pantry_employee_id= fields.Char(string="Mã Nhân Viên Pantry")
    is_pantry_manager = fields.Boolean(string="Là quản lý Pantry")
    pantry_allowance = fields.Float(string="Phụ cấp ăn uống")

    @api.model
    def create_test_pantry_employee(self, name, pantry_code):
        """
        Ví dụ về @api.model:
        Hàm này không cần gọi từ một bản ghi cụ thể (recordset),
        mà gọi trực tiếp từ model (class).
        Thường dùng để tạo mới record hoặc xử lý logic chung.
        """
        # self ở đây là Model (hr.employee), không phải là một record cụ thể
        new_employee = self.create({
            'name': name,
            'pantry_employee_id': pantry_code,
            'pantry_allowance': 500000.0, # Mặc định
        })
        return new_employee