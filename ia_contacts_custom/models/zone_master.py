from odoo import api, models, fields, _


class ZoneMaster(models.Model):
    _name = "zone.master"

    name = fields.Char(string="Zone")
    sale_teams_id = fields.Many2one('crm.team', string='Sales Team')