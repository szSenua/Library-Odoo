from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Add a boolean field to indicate if the partner is an author
    is_author = fields.Boolean(string='Is Author', default=False)