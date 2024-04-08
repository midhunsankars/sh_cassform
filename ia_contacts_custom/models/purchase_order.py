from odoo import api, fields, models, _
from math import ceil


class PurchaseOrderLineInherited(models.Model):
    _inherit = 'purchase.order.line'

    product_id = fields.Many2one('product.product', string='Product', domain=['|', ('purchase_ok', '=', True),('rent_ok', '=', True)], change_default=True, index='btree_not_null')

class PurchaseOrderInherited(models.Model):
    _inherit = 'purchase.order'

    rental_start_date = fields.Datetime(string="Rental Start Date", tracking=True,  default=fields.datetime.today())
    rental_return_date = fields.Datetime(string="Rental Return Date", tracking=True)
    stock_id = fields.Many2one('stock.picking', string="Delivery Order")
    return_order_id = fields.Many2one('stock.picking', string="Returned Order")
    picking_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Receptions', copy=False, store=True)

    # @api.depends('rental_start_date', 'rental_return_date')
    # def _compute_duration(self):
    #     self.duration_days = 0
    #     self.remaining_hours = 0
    #     for order in self:
    #         if order.rental_start_date and order.rental_return_date:
    #             duration = order.rental_return_date - order.rental_start_date
    #             order.duration_days = duration.days
    #             order.remaining_hours = ceil(duration.seconds / 3600)

    def button_confirm(self):
        res = super(PurchaseOrderInherited, self).button_confirm()
        for rec in self.picking_ids:
            rec.write({'scheduled_date': self.rental_return_date,
                       'move_line_ids': [(6, 0, self.stock_id.move_ids.move_line_ids.ids)]})
            print("recrec", rec.picking_type_id.name)
            return_order_values = {
                'location_id': rec.location_dest_id.id,
                'location_dest_id': self.env.ref('stock.stock_location_suppliers').id,
                'picking_type_id': self.env.ref('stock.picking_type_in').id,
                'partner_id': rec.partner_id.id,
                'origin': self.name,
                'date_deadline': rec.date_deadline,
                'group_id': rec.group_id.id
            }
            return_order = self.env['stock.picking'].create(return_order_values)
            self.write({'return_order_id': return_order.id})
            self.picking_ids = [(4, return_order.id)]
            for lines in rec.move_ids:
                lines.write({'date_deadline': self.rental_return_date,
                             'move_line_ids': [(6, 0, self.stock_id.move_ids.move_line_ids.ids)]})
                return_order_line_values = {
                    'quantity': lines.product_qty,
                    'picking_id': return_order.id,
                    'product_id': lines.product_id.id,
                    'name': lines.product_id.name,
                    'product_uom_qty': lines.product_uom_qty,
                    'location_id': rec.location_dest_id.id,
                    'location_dest_id': rec.location_id.id,
                    'date_deadline': self.rental_return_date,
                }
                self.env['stock.move'].create(return_order_line_values)
            return_order.write({'state': 'waiting', 'scheduled_date': self.rental_return_date,
                                'move_line_ids': [(6, 0, self.stock_id.move_ids.move_line_ids.ids)]})
        return res

