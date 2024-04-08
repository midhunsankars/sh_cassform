from odoo import api, models, fields, _


class ZoneMaster(models.Model):
    _name = "post.code.master"

    name = fields.Char(string="Post Code")
    zone = fields.Many2one('zone.master', string="Zone")