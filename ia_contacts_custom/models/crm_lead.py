from xml import etree

from odoo import api, models, fields, _



class CrmLead(models.Model):
    _inherit = "crm.lead"

    product_category = fields.Many2many('product.category', string="Product Category")
    post_code = fields.Many2one('post.code.master', string="Post Code")
    is_referral = fields.Boolean(string="Is Referral")
    is_postcode = fields.Boolean(string="Is Postcode" )

    @api.onchange('post_code')
    def _onchange_post_code(self):
        if self.post_code:
            sales_team_id = self.post_code.zone.sale_teams_id.id
            post_code = self.post_code.name
            if sales_team_id:
                self.is_postcode = True
                self.write({'team_id': sales_team_id,'zip': post_code})
            else:
                self.write({'team_id': False})

    # Add sales team members to the followers
    @api.model_create_multi
    def create(self, vals_list):
        sales_team = super(CrmLead, self).create(vals_list)
        for record in sales_team.team_id.member_ids:
            followers = []
            if record.partner_id.id not in record.message_follower_ids.ids:
                followers.append(record.partner_id.id)
            sales_team.message_subscribe(followers)
        return sales_team
