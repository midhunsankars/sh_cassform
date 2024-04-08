from odoo import api, models, fields, _

from odoo.exceptions import ValidationError
import math
class SaleOrderInherit(models.Model):

    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        res = super(SaleOrderInherit, self)._create_invoices()
        total_cross_hire_qty = 0
        for rec in self.order_line:
            total_qty = rec.product_uom_qty
            stock_moves = self.mapped('picking_ids').move_ids
            for stock in stock_moves.move_line_ids:
                if stock.result_package_id.is_cross_hire and stock.state == "done":
                    total_cross_hire_qty = sum(stock.mapped('quantity'))
            if total_qty > 0:
                cross_hire_percentage = (total_cross_hire_qty / total_qty) * 100
                print("cross_hire_percentage", cross_hire_percentage)
                if cross_hire_percentage > 0:
                    cross_hire_analytic_accounts = self.env['account.analytic.account'].search(
                                                                    [('name', '=', "Cross Hire")])
                    own_hire_analytic_accounts = self.env['account.analytic.account'].search(
                        [('name', '=', "Own Hire")])
                    hire_percentage = int(cross_hire_percentage)
                    own_percentage = 100 - hire_percentage
                    rec.invoice_lines.write({'analytic_distribution': {
                            cross_hire_analytic_accounts.id: hire_percentage,
                            own_hire_analytic_accounts.id: own_percentage
                        }})
        return res