from odoo import models, fields, api
from datetime import date

class PantryCheck(models.Model):
    _name = 'pantry.check'
    _description = 'Phiếu kiểm kho'
    _order = 'date desc, id desc'

    name = fields.Char(string="Mã phiếu", required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string="Ngày kiểm", default=fields.Date.context_today, required=True)
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('done', 'Đã xác nhận')
    ], string="Trạng thái", default='draft')
    
    line_ids = fields.One2many('pantry.check.line', 'check_id', string="Chi tiết")
    
    total_revenue = fields.Monetary(string="Tổng doanh thu", compute='_compute_total_profit', currency_field='currency_id')
    total_cost = fields.Monetary(string="Tổng vốn", compute='_compute_total_profit', currency_field='currency_id')
    total_discard_cost = fields.Monetary(string="Tổng chi phí hủy", compute='_compute_total_profit', currency_field='currency_id')
    total_profit = fields.Monetary(string="Tổng lãi/lỗ", compute='_compute_total_profit', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Tiền tệ", default=lambda self: self.env['res.currency'].search([('name', '=', 'VND')], limit=1))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('pantry.check') or 'New'
        return super(PantryCheck, self).create(vals_list)

    @api.depends('line_ids.profit', 'line_ids.revenue', 'line_ids.cost', 'line_ids.discard_cost')
    def _compute_total_profit(self):
        for record in self:
            record.total_revenue = sum(line.revenue for line in record.line_ids)
            record.total_cost = sum(line.cost for line in record.line_ids)
            record.total_discard_cost = sum(line.discard_cost for line in record.line_ids)
            record.total_profit = sum(line.profit for line in record.line_ids)





    def action_load_items(self):
        self.ensure_one()
        # Clear existing lines
        self.line_ids.unlink()
        
        items = self.env['pantry.item'].search([])
        lines = []
        for item in items:
            lines.append((0, 0, {
                'item_id': item.id,
                'system_qty': item.quantity,
                'actual_qty': item.quantity, # Default to system qty
            }))
        self.write({'line_ids': lines})

    def action_confirm(self):
        self.ensure_one()
        for line in self.line_ids:
            # Update stock in pantry.item
            line.item_id.quantity = line.actual_qty
        self.write({'state': 'done'})
