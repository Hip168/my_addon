# my_employee_extension/__manifest__.py
{
    'name': "Employee Student ID Extension",
    'summary': "Thêm trường Mã Sinh Viên vào hồ sơ nhân viên.",
    'author': "Tên của bạn",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': [
        'base', 
        'hr'  # <--- Module Nhân viên của Odoo
    ],
    'data': [
        'views/views.xml',
    ],
    # ...
}