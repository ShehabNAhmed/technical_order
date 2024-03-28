from odoo import models, fields, api, _

class resparnter(models.Model):
    _inherit = 'res.partner'

    is_tech_offer = fields.Boolean( string='is_tech_offer')

