from odoo import models, fields, api

class PantryItem(models.Model):
    _name = 'pantry.item'
    _description = 'Pantry Item'

    name = fields.Char(string="Tên sản phẩm", required=True)
    
    # Currency
    currency_id = fields.Many2one('res.currency', string="Tiền tệ", default=lambda self: self.env['res.currency'].search([('name', '=', 'VND')], limit=1))

    # Import Info
    import_price = fields.Monetary(string="Giá nhập", currency_field='currency_id')
    import_uom = fields.Char(string="Đơn vị nhập", default="Thùng")
    
    # Sale Info
    sale_price = fields.Monetary(string="Giá bán", currency_field='currency_id')
    sale_uom = fields.Char(string="Đơn vị bán", default="Cái")
    sale_qty = fields.Float(string="Số lượng bán", default=1.0, help="Số lượng đơn vị bán trong 1 lần bán (ví dụ: bán theo cặp thì nhập 2).")
    
    # Conversion
    conversion_rate = fields.Float(string="Tỷ lệ quy đổi", default=1.0, help="1 Đơn vị nhập bằng bao nhiêu Đơn vị bán?")
    conversion_info = fields.Char(string="Diễn giải quy đổi", compute='_compute_conversion_info')
    
    # Inventory
    quantity = fields.Float(string="Tồn kho (Đơn vị bán)", default=0.0, readonly=True)
    
    # Transient field for initial stock input
    initial_stock = fields.Float(string="Tồn kho ban đầu (Đơn vị bán)", help="Nhập số lượng tồn kho ban đầu theo Đơn vị bán.")

    @api.depends('import_uom', 'sale_uom', 'conversion_rate')
    def _compute_conversion_info(self):
        for record in self:
            i_uom = record.import_uom or '...'
            s_uom = record.sale_uom or '...'
            rate = record.conversion_rate
            record.conversion_info = f"1 {i_uom} = {rate:g} {s_uom}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('initial_stock', 0) > 0:
                # Direct assignment, no conversion needed as input is already in Sale Unit
                vals['quantity'] = vals['initial_stock']
        return super(PantryItem, self).create(vals_list)
