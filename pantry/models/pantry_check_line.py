from odoo import models, fields, api
from datetime import date
class PantryCheckLine(models.Model):
    _name = 'pantry.check.line'
    _description = 'Chi tiết kiểm kho'

    check_id = fields.Many2one('pantry.check', string="Phiếu kiểm", required=True, ondelete='cascade')
    item_id = fields.Many2one('pantry.item', string="Sản phẩm", required=True)
    currency_id = fields.Many2one(related='check_id.currency_id')
    
    date = fields.Date(related='check_id.date', string="Ngày kiểm", store=True)
    
    system_qty = fields.Float(string="Tồn hệ thống", compute='_compute_system_qty', store=True, readonly=True)
    actual_qty = fields.Float(string="Thực tế", required=True)
    discard_qty = fields.Float(string="Hủy/Hỏng", default=0.0)
    
    sold_qty = fields.Float(string="Đã bán", compute='_compute_sold_profit', store=True)
    
    cost = fields.Monetary(string="Vốn", compute='_compute_sold_profit', currency_field='currency_id', store=True)
    discard_cost = fields.Monetary(string="Chi phí hủy", compute='_compute_sold_profit', currency_field='currency_id', store=True)
    revenue = fields.Monetary(string="Doanh thu", compute='_compute_sold_profit', currency_field='currency_id', store=True)
    profit = fields.Monetary(string="Lãi/Lỗ", compute='_compute_sold_profit', currency_field='currency_id', store=True)
    

    @api.depends('item_id')
    def _compute_system_qty(self):
        for line in self:
            line.system_qty = line.item_id.quantity
    

    @api.depends('system_qty', 'actual_qty', 'discard_qty', 'item_id')
    def _compute_sold_profit(self):
        for line in self:
            # Sold = System - Actual - Discard
            sold = line.system_qty - line.actual_qty - line.discard_qty
            line.sold_qty = sold
            
            # Calculate Cost per Sale Unit
            import_price_per_sale_unit = 0
            if line.item_id.conversion_rate:
                import_price_per_sale_unit = line.item_id.import_price / line.item_id.conversion_rate
            
            # Discard Cost
            line.discard_cost = line.discard_qty * import_price_per_sale_unit

            # Cost = (Sold + Discard) * Import Price (converted)
            # We paid for both sold and discarded items
            line.cost = (sold + line.discard_qty) * import_price_per_sale_unit
            
            # Revenue = Sold * Sale Price
            line.revenue = sold * line.item_id.sale_price
            
            # Profit = Revenue - Cost
            line.profit = line.revenue - line.cost


