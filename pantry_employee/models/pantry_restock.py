from odoo import models, fields, api
from datetime import date

class PantryRestock(models.Model):
    _name = 'pantry.restock'
    _description = 'Phiếu nhập hàng'
    _order = 'date desc, id desc'

    name = fields.Char(string="Mã phiếu", required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string="Ngày nhập", default=fields.Date.context_today, required=True)
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('done', 'Đã nhập kho')
    ], string="Trạng thái", default='draft')
    
    line_ids = fields.One2many('pantry.restock.line', 'restock_id', string="Chi tiết")
    
    total_amount = fields.Monetary(string="Tổng tiền", compute='_compute_total_amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Tiền tệ", default=lambda self: self.env['res.currency'].search([('name', '=', 'VND')], limit=1))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('pantry.restock') or 'New'
        return super(PantryRestock, self).create(vals_list)

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.line_ids)

    def action_confirm(self):
        self.ensure_one()
        for line in self.line_ids:
            # Convert Import Unit to Sale Unit
            conversion = line.item_id.conversion_rate or 1.0
            qty_to_add = line.quantity * conversion
            
            # Update stock
            line.item_id.quantity += qty_to_add
            
            # Optional: Update Import Price if changed? 
            # For now, let's keep it simple and just update stock.
            
        self.write({'state': 'done'})
