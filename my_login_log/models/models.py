# --- PHẦN QUAN TRỌNG NHẤT: IMPORT THƯ VIỆN ---
from odoo import models, fields, api
import logging
import csv
import os
from datetime import datetime, timedelta  # <--- BẠN ĐANG THIẾU DÒNG NÀY

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_export_recent_logins_to_csv(self):
        _logger.info(">>> BẮT ĐẦU quy trình xuất file CSV user login...")

        # 1. DATETIME
        # Bây giờ Odoo mới hiểu datetime là gì nhờ dòng import ở trên
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        
        # 2. TÌM KIẾM
        recent_users = self.search([
            ('login_date', '>=', seven_days_ago)
        ])
        
        # Kiểm tra nếu không có user nào
        if not recent_users:
            _logger.warning("Không tìm thấy user nào đăng nhập trong 7 ngày qua.")
            return

        # 3. ĐƯỜNG DẪN FILE
        directory = '/tmp'
        # Dòng này lúc nãy bị lỗi vì thiếu 'datetime', giờ sẽ chạy ngon
        filename = f"log_login_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        file_path = os.path.join(directory, filename)

        try:
            # 4. GHI CSV
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['User ID', 'Tên hiển thị', 'Email/Login', 'Thời gian đăng nhập'])
                
                count = 0
                for user in recent_users:
                    writer.writerow([
                        user.id, 
                        user.name, 
                        user.login, 
                        user.login_date
                    ])
                    count += 1
            
            _logger.info(f"Đã xuất thành công {count} user vào file: {file_path}")
            
        except Exception as e:
            _logger.error(f"Lỗi: {e}")