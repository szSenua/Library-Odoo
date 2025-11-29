from odoo import _, fields, models, api

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

    # See the loans associated with this book
    loan_ids = fields.One2many(
        'library.loan', 
        'book_id', 
        string='Loans')
    
    # Calculate if the book is currently available
    is_available = fields.Boolean(
        string='Is Available',
        compute='_compute_is_available',
        store=True)
    
    # Compute method to determine availability
    @api.depends('loan_ids.state')
    def _compute_is_available(self):
        for book in self:
            # Check if there are any ongoing loans for this book
            ongoing_loans = book.loan_ids.filtered(lambda loan: loan.state == 'ongoing')
            # If there are no ongoing loans, the book is available
            book.is_available = len(ongoing_loans) == 0

    
