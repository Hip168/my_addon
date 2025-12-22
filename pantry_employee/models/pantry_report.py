from odoo import models, fields, tools

class PantryReport(models.Model):
    _name = "pantry.report"
    _description = "Báo cáo Doanh thu & Lãi lỗ"
    _auto = False
    _order = 'date desc'

    date = fields.Date(string="Ngày", readonly=True)
    item_id = fields.Many2one('pantry.item', string="Sản phẩm", readonly=True)
    
    # Import (Restock)
    import_qty = fields.Float(string="SL Nhập", readonly=True)
    import_cost = fields.Float(string="Chi phí Nhập", readonly=True)
    
    # Export (Check/Sales)
    sold_qty = fields.Float(string="SL Bán", readonly=True)
    revenue = fields.Float(string="Doanh thu", readonly=True)
    cogs = fields.Float(string="Giá vốn hàng bán", readonly=True)
    
    # Discard
    discard_qty = fields.Float(string="SL Hủy", readonly=True)
    discard_cost = fields.Float(string="Chi phí Hủy", readonly=True)
    
    # Profit
    profit = fields.Float(string="Lợi nhuận", readonly=True)

    type = fields.Selection([
        ('import', 'Nhập hàng'),
        ('sale', 'Bán hàng')
    ], string="Loại", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () as id,
                    sub.date,
                    sub.item_id,
                    sub.type,
                    SUM(sub.import_qty) as import_qty,
                    SUM(sub.import_cost) as import_cost,
                    SUM(sub.sold_qty) as sold_qty,
                    SUM(sub.revenue) as revenue,
                    SUM(sub.cogs) as cogs,
                    SUM(sub.discard_qty) as discard_qty,
                    SUM(sub.discard_cost) as discard_cost,
                    SUM(sub.profit) as profit
                FROM (
                    -- RESTOCK DATA
                    SELECT
                        l.date as date,
                        l.item_id as item_id,
                        'import' as type,
                        l.quantity as import_qty,
                        l.subtotal as import_cost,
                        0 as sold_qty,
                        0 as revenue,
                        0 as cogs,
                        0 as discard_qty,
                        0 as discard_cost,
                        0 as profit
                    FROM pantry_restock_line l
                    JOIN pantry_restock r ON l.restock_id = r.id
                    WHERE r.state = 'done'

                    UNION ALL

                    -- CHECK DATA
                    SELECT
                        l.date as date,
                        l.item_id as item_id,
                        'sale' as type,
                        0 as import_qty,
                        0 as import_cost,
                        l.sold_qty as sold_qty,
                        l.revenue as revenue,
                        l.cost as cogs,
                        l.discard_qty as discard_qty,
                        l.discard_cost as discard_cost,
                        l.profit as profit
                    FROM pantry_check_line l
                    JOIN pantry_check c ON l.check_id = c.id
                    WHERE c.state = 'done'
                ) sub
                GROUP BY sub.date, sub.item_id, sub.type
            )
        """ % self._table)
