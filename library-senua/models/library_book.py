from odoo import _, fields, models

class LibraryBook(models.Model):
    # Book model definition
    _name = 'library.book'

    # Book model description
    _description = 'Library Book'
    

    # Book name field
    name = fields.Char(string='Title', required=True)

    # Book date field
    release_date = fields.Date(string='Release Date')

    # Book ISBN field
    isbn = fields.Char(string='ISBN')

    # Book author field with domain filter, res partner means it links to contacts model
    author_id = fields.Many2one(
        'res.partner', string='Author', domain=[('is_company', '=', True)])
    
    # Book summary field
    summary = fields.Text(string='Summary')

    # Book cover field
    cover = fields.Image(string='Book Cover')
    
