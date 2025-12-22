# my_employee_extension/models/models.py
from odoo import fields, models

class HREmployeeExtension(models.Model):
    # Kế thừa Model nhân viên gốc
    _inherit = 'hr.employee' 
    
    # Thêm trường Mã Sinh Viên
    ma_sinh_vien = fields.Char(
        string='Mã Sinh Viên',
        copy=False,  # Ngăn không cho trường này được sao chép khi nhân bản hồ sơ
        help='Mã số sinh viên (nếu có).'
    )