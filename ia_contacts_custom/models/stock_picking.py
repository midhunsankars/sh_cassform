from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_purchase_order_created = fields.Boolean(string="Purchase Order", default=False)

    def action_create_purchase_order(self):
        print("purchase order")
        order_list = []
        rental_orders = self.env['sale.order'].search([('name', '=', self.origin), ('is_rental_order', '=', True)])
        if rental_orders:
            for rentals in rental_orders:
                for line in rentals.order_line:
                    for rec in self.move_ids.move_line_ids:
                        print("rec", rec.result_package_id)
                        if rec.result_package_id.is_cross_hire:
                            self.write({'is_purchase_order_created': True})
                            order = self.env['purchase.order'].create({
                                'partner_id': self.partner_id.id,
                                'stock_id': self.id,
                                'rental_start_date': rentals.rental_start_date,
                                'rental_return_date': rentals.rental_return_date,
                                'order_line': [(0, 0, {
                                    'name': rec.product_id.name,
                                    'product_id': rec.product_id.id,
                                    'product_qty': rec.move_id.quantity,
                                    'price_unit': line.price_unit,
                                })],
                            })
                            print("orderrr", order)
                            purchases = self.env['purchase.order'].sudo().search([('stock_id.name', '=', self.name)], limit=1).id
                            print("purchase", purchases)
                            if purchases:
                                order_list.append(purchases)

                            value = {
                                'type': 'ir.actions.act_window',
                                'name': 'Purchase Order',
                                'view_type': 'form',
                                'view_mode': 'tree,form',
                                'domain': [("id", "in", order_list)],
                                'res_model': 'purchase.order',
                            }
                            return value
                        if not rec.result_package_id.is_cross_hire:
                            raise ValidationError("order can only be created by products that have been cross hired")

