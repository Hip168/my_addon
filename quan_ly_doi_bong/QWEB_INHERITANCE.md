# Hướng dẫn QWeb Inheritance (Kế thừa) - Dựa trên `football_report.xml`

Tài liệu này giải thích cơ chế kế thừa trong Odoo QWeb thông qua ví dụ thực tế trên file báo cáo cầu thủ (`football_report.xml`) mà chúng ta đang làm việc.

## 1. Cấu trúc Template Gốc
Template hiện tại của chúng ta có ID là `report_player_profile` nằm trong module `quan_ly_doi_bong`.

**XML ID đầy đủ:** `quan_ly_doi_bong.report_player_profile`

```xml
<!-- Code gốc tóm tắt -->
<template id="report_player_profile">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.basic_layout">
                <div class="page" style="...">
                    <!-- Khối 1: Alert Success -->
                    <div class="alert alert-success">
                        <h4>1. Demo t-field...</h4>
                        <p>Tên cầu thủ: <span t-field="o.name" .../></p>
                        ...
                    </div>
                    
                    <!-- Khối 2: Alert Info -->
                    <div class="alert alert-info">...</div>
                </div>
            </t>
        </t>
    </t>
</template>
```

---

## 2. Các Kịch bản Kế thừa Thực tế

Giả sử bạn (hoặc một module khác) muốn chỉnh sửa báo cáo này mà **KHÔNG** muốn sửa trực tiếp vào file `football_report.xml` gốc. Chúng ta sẽ tạo một file XML mới và dùng cơ chế kế thừa (`inherit_id`).

### Kịch bản A: Thêm trường "Vị trí" vào sau "Tên cầu thủ" (Dùng `position="after"`)

Chúng ta muốn thêm dòng `<p>Vị trí: <span t-field="o.position"/></p>` ngay sau dòng Tên cầu thủ.

```xml
<odoo>
    <template id="report_player_profile_inherit_position" inherit_id="quan_ly_doi_bong.report_player_profile">
        <!-- Tìm thẻ span hiển thị tên cầu thủ -->
        <xpath expr="//span[@t-field='o.name']/.." position="after">
            <p>Vị trí: <span t-field="o.position"/></p>
        </xpath>
    </template>
</odoo>
```
*Giải thích:*
*   `inherit_id`: Trỏ về template gốc.
*   `expr="//span[@t-field='o.name']/.."`: Tìm thẻ cha (`<p>`) của thẻ span tên.
*   `position="after"`: Chèn đoạn code mới vào sau thẻ `<p>` đó.

### Kịch bản B: Ẩn/Xóa phần "Demo t-esc" màu xanh dương (Dùng `position="replace"`)

Chúng ta muốn bỏ khối `<div class="alert alert-info">` đi.

```xml
<odoo>
    <template id="report_player_profile_remove_demo" inherit_id="quan_ly_doi_bong.report_player_profile">
        <!-- Tìm div có class là alert-info -->
        <xpath expr="//div[hasclass('alert-info')]" position="replace">
            <!-- Để trống bên trong nghĩa là thay thế bằng "hư vô" -> Xóa -->
            <comment>Đã xóa phần Demo t-esc</comment>
        </xpath>
    </template>
</odoo>
```

### Kịch bản C: Đổi màu tiêu đề thành màu đỏ (Dùng `position="attributes"`)

Thay vì màu xanh đậm (`darkblue`) trong code gốc, chúng ta muốn đổi tiêu đề "1. Demo t-field..." thành màu đỏ (`red`).

```xml
<odoo>
    <template id="report_player_profile_change_color" inherit_id="quan_ly_doi_bong.report_player_profile">
        <!-- Tìm thẻ h4 bên trong div success -->
        <xpath expr="//div[hasclass('alert-success')]/h4" position="attributes">
            <!-- Ghi đè thuộc tính style -->
            <attribute name="style">font-weight: bold; color: red;</attribute>
        </xpath>
    </template>
</odoo>
```

---

## 3. Cách xác định XPath chính xác

Để tính năng kế thừa hoạt động, quan trọng nhất là bạn phải "trỏ" đúng vị trí bằng XPath.

1.  **Theo thuộc tính duy nhất (Khuyên dùng):**
    *   `//span[@t-field='o.name']`: Rất chính xác vì `t-field` thường duy nhất trong 1 ngữ cảnh.
    *   `//div[@id='my_unique_div']`: Nếu trong code gốc bạn đã đặt ID.

2.  **Theo Class CSS:**
    *   `//div[hasclass('alert-success')]`: Tìm thẻ div có class này.

3.  **Theo cấu trúc (Dễ gãy nếu cấu trúc đổi):**
    *   `/t/t/t/div/div[1]`: Tìm thẻ div con đầu tiên bên trong cấu trúc lồng nhau. Cách này **không nên dùng** vì nếu ai thêm 1 thẻ div bao ngoài thì xpath này sẽ sai ngay.

## 4. Tổng kết
Việc sử dụng kế thừa (Inheritance) giúp bạn:
1.  Giữ nguyên code gốc (Code sạch).
2.  Dễ dàng nâng cấp module gốc mà không mất các chỉnh sửa riêng.
3.  Cho phép nhiều module cùng chỉnh sửa một báo cáo (Ví dụ: Module A thêm Logo, Module B thêm Chữ ký).
