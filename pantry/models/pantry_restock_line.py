from odoo import models, fields, api

class PantryRestockLine(models.Model):
    _name = 'pantry.restock.line'
    _description = 'Chi tiết nhập hàng'

    restock_id = fields.Many2one('pantry.restock', string="Phiếu nhập", required=True, ondelete='cascade')
    item_id = fields.Many2one('pantry.item', string="Sản phẩm", required=True)
    currency_id = fields.Many2one(related='restock_id.currency_id')
    
    date = fields.Date(related='restock_id.date', string="Ngày nhập", store=True)
    
    quantity = fields.Float(string="Số lượng (Đơn vị nhập)", required=True, default=1.0)
    import_uom = fields.Char(related='item_id.import_uom', string="ĐVT", readonly=True)
    
    price_unit = fields.Monetary(string="Đơn giá nhập", required=True, currency_field='currency_id')
    subtotal = fields.Monetary(string="Thành tiền", compute='_compute_subtotal', currency_field='currency_id', store=True)

    @api.onchange('item_id')
    def _onchange_item_id(self):
        if self.item_id:
            self.price_unit = self.item_id.import_price

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
