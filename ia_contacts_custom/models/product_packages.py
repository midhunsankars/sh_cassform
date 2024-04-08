from odoo import api, fields, models, _


class ProductPackages(models.Model):
    _inherit = "stock.quant.package"

    is_cross_hire = fields.Boolean(string="Cross Hire")

