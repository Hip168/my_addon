from odoo import models, fields, api
from datetime import datetime


class SinhVien(models.Model):
    _name = "sinh_vien.sinh_vien"
    _description = "Sinh Viên"
    _rec_name = "student_code"

    student_code = fields.Char(
        string="Mã Sinh Viên",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: ("Mới"),
    )

    def _compute_display_name(self):
        for record in self:
            record.display_name = (
                f"[{record.student_code}] {record.name}"
                if record.name
                else record.student_code
            )

    name = fields.Char(string="Họ Tên")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("student_code", "Mới") == "Mới":
                vals["student_code"] = (
                    self.env["ir.sequence"].next_by_code("sinh_vien.sinh_vien") or "Mới"
                )
        return super(SinhVien, self).create(vals_list)

    # Quan hệ với bảng trung gian
    student_class_ids = fields.One2many(
        "sinh_vien.student_class_rel", "student_id", string="Lớp đã tham gia"
    )

    date_of_birth = fields.Date(string="Ngày sinh")
    age = fields.Integer(string="Tuổi", compute="_compute_age", store=True)
    gender = fields.Selection([("male", "Nam"), ("female", "Nữ")], string="Giới tính")
    address = fields.Text(string="Địa chỉ")
    phone = fields.Char(string="Số điện thoại")
    email = fields.Char(string="Email")

    @api.depends("date_of_birth")
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                record.age = (datetime.now().date() - record.date_of_birth).days // 365
            else:
                record.age = 0


class LopHoc(models.Model):
    _name = "sinh_vien.class"
    _description = "Lớp Học"

    name = fields.Char(string="Tên Lớp")
    # Quan hệ với bảng trung gian
    student_ids = fields.One2many(
        "sinh_vien.student_class_rel", "class_id", string="Danh sách sinh viên"
    )


class StudentClassRel(models.Model):
    _name = "sinh_vien.student_class_rel"
    _description = "Bảng trung gian Sinh viên - Lớp"

    student_id = fields.Many2one(
        "sinh_vien.sinh_vien", string="Sinh viên", required=True
    )
    class_id = fields.Many2one("sinh_vien.class", string="Lớp", required=True)

    # Các trường bổ sung cho bảng trung gian
    date_start = fields.Date(string="Ngày bắt đầu", default=fields.Date.today)
    date_end = fields.Date(string="Ngày kết thúc")
    is_active = fields.Boolean(string="Đang học", default=True)
    grade = fields.Float(string="Điểm số")
    note = fields.Text(string="Ghi chú")
