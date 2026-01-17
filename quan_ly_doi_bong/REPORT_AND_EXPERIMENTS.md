# Báo cáo và Thực nghiệm: CORS, API Depends/Onchange, và Many2many Fields

## 1. Tìm hiểu về CORS (Cross-Origin Resource Sharing)

### Khái niệm
CORS là cơ chế bảo mật của trình duyệt ngăn chặn web page từ một domain (origin) này thực hiện call API tới một domain khác nếu server không cho phép.

### Trong Odoo
Odoo hỗ trợ CORS thông qua tham số `cors` trong decorator `@http.route`.
- `cors='*'` : Cho phép tất cả các domain truy cập.
- `cors='http://my-client-app.com'` : Chỉ cho phép domain cụ thể.

### Thực nghiệm
Đã tạo 2 API trong `controllers/main.py`:
1. `/football/players`: Có `cors='*'`.
2. `/football/teams`: Không set CORS (mặc định).

**Kịch bản thử nghiệm:**
Mở Developer Console (F12) trên một trang web bất kỳ (ví dụ `google.com`) và chạy đoạn code sau:

```javascript
// Test CORS Success
fetch('http://localhost:8069/football/players', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({jsonrpc: "2.0", params: {}})
}).then(r => r.json()).then(console.log).catch(console.error);

// Test CORS Fail (nếu browser chặn strict)
fetch('http://localhost:8069/football/teams', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({jsonrpc: "2.0", params: {}})
}).then(r => r.json()).then(console.log).catch(console.error);
```

## 2. Thực nghiệm @api.depends và onchange nhiều cấp

### Yêu cầu
Xử lý sự phụ thuộc dữ liệu qua nhiều cấp quan hệ.

### Thực hiện
1. **Level 1 Dependency**:
   - Model: `football.player`
   - Field: `coach_name`
   - Logic: `@api.depends('team_id.coach_name')`. Khi HLV của đội thay đổi, tên HLV trên hồ sơ cầu thủ tự cập nhật.

2. **Level 2 Dependency (Deep)**:
   - Model: `football.match`
   - Field: `home_team_value`
   - Logic: `@api.depends('team_home_id.total_salary')`.
     - `team_home_id` trỏ tới `football.team`.
     - `football.team.total_salary` lại depends vào `player_ids.salary`.
     - Kết quả: Khi thay đổi lương của một cầu thủ (Level 3) -> Tổng lương đội cập nhật (Level 2) -> Giá trị đội chủ nhà trong trận đấu cập nhật (Level 1).

3. **Onchange**:
   - Model: `football.player`
   - Logic: Thay đổi `position` hoặc `salary` sẽ tự động tính `suggested_bonus`.

## 3. Kịch bản Many2many với các trường bổ sung

### Vấn đề
Mối quan hệ Many2many mặc định của Odoo (ví dụ: `Match` <-> `Player`) chỉ lưu trữ ID của 2 bên mà không thể lưu thêm dữ liệu như "Số bàn thắng", "Số phút thi đấu" trong trận đó.

### Giải pháp
Sử dụng mô hình trung gian (Intermediary Model).

### Kịch bản Tạo thêm trường
**Tên kịch bản**: Quản lý đội hình ra sân và hiệu suất thi đấu.

**Yêu cầu cần đạt**:
- Người dùng có thể chọn danh sách cầu thủ tham gia trận đấu.
- Với mỗi cầu thủ, có thể nhập: Số bàn thắng, Kiến tạo, Số phút thi đấu.
- Dữ liệu này gắn liền với *Trận đấu cụ thể* đó.

**Kịch bản thử nghiệm**:
1. Vào menu **Matches**, tạo một trận đấu mới.
2. Tại tab "Lineup & Stats", nhấn "Add a line".
3. Chọn cầu thủ "Nguyen Van A".
4. Nhập Goals: 2, Assists: 1.
5. Lưu trận đấu.
6. Kết quả: Dữ liệu bàn thắng được lưu trữ riêng cho trận đấu này. Nếu "Nguyen Van A" đá trận khác, dữ liệu sẽ mới hoàn toàn.

**Kết quả**:
- Model `football.match.lineup` đã được tạo để giải quyết vấn đề này.
- Giao diện cho phép nhập liệu trực tiếp trên form Trận đấu (One2many editable list).

