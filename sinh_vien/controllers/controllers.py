import json
from odoo import http
from odoo.http import request


class SinhVienController(http.Controller):

    @http.route(
        "/sinh_vien/api/list",
        auth="public",
        type="http",
        cors="*",
        methods=["GET", "POST"],
        csrf=False,
    )
    def list_sinh_vien(self, **kw):
        """
        API trả về danh sách sinh viên.
        - type='http': Trả về JSON chuẩn, có thể test trực tiếp trên trình duyệt bằng method GET.
        - cors='*': Cho phép gọi từ mọi nguồn.
        - csrf=False: Tắt bảo vệ CSRF để gọi API dễ dàng hơn từ bên ngoài.
        """
        students = request.env["sinh_vien.sinh_vien"].sudo().search([])
        data = []
        for s in students:
            data.append(
                {
                    "student_code": s.student_code,
                    "name": s.name,
                    "age": s.age,
                    "gender": s.gender,
                    "email": s.email,
                }
            )

        # Trả về response JSON chuẩn
        return request.make_response(
            json.dumps(
                {"status": "success", "count": len(data), "data": data},
                ensure_ascii=False,
            ),
            headers=[("Content-Type", "application/json")],
        )
