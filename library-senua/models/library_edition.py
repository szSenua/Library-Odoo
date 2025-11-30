from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryEdition(models.Model):
    _name = 'library.edition'
    _description = 'Library Edition'
    # Default ordering by year descending
    _order = 'year desc'
    
   # Book reference
    book_id = fields.Many2one('library.book', string='Book', required=True)

    # Edition year
    year = fields.Char(string='Edition Year', required=True)

    # Number of copies available
    copies = fields.Integer(string='Number of Copies', default=1)

    # Display name combining book title and edition year
    name = fields.Char(
        string='Edition Name',
        compute='_compute_name',
        store=True
        )
    
    @api.depends('copies', 'year')
    def _compute_name(self):
        for edition in self:
           edition.name = f"{edition.year} Edition ({edition.copies} copies)"