import re

from odoo import api, models, fields, _

from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    type = fields.Selection(selection_add=[('site_address', 'Site Address')])
    post_codes = fields.Many2one('post.code.master', string="Post Code")
    is_postcode = fields.Boolean(string="Is Postcode")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('email'):
                contacts_mail = vals.get('email')
                contacts_exists = self.env["res.partner"].search([("email", "=", contacts_mail)])
                if contacts_exists:
                    raise ValidationError(_('Contacts with this Email ID Already exists.'))
            if vals.get('phone'):
                phone = vals.get('phone')
                # pattern = r'^(\+61|04)\d{8}$'
                # cleaned_number = phone.replace("+", "")
                # phone_no = cleaned_number
                print("len(phone)", len(phone))
                if len(phone) < 11 :
                    raise ValidationError(_('Phone number is not valid.'))
                # if not re.match(pattern, phone):
                #     raise ValidationError(_('Phone number should be starts with either  04 nor  +61.'))
        partner = super(ResPartner, self).create(vals_list)
        #  # Add sales team members to the followers
        for record in partner.team_id.member_ids:
            followers = []
            if record.partner_id.id not in record.message_follower_ids.ids:
                followers.append(record.partner_id.id)
            partner.message_subscribe(followers)

        return partner

    @api.onchange('post_codes')
    def _onchange_post_code(self):
        if self.post_codes:
            sales_team_id = self.post_codes.zone.sale_teams_id.id
            post_code = self.post_codes.name
            if sales_team_id:
                self.is_postcode = True
                self.write({'team_id': sales_team_id, 'zip': post_code})
            else:
                self.write({'team_id': False})
