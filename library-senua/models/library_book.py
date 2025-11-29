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
    
    # Book status based on loan state
    state = fields.Selection([
        ('available', 'Available'),
        ('loaned', 'On Loan'),
        ('overdue', 'Overdue')
    ], string='Status', compute='_compute_state', store=True, readonly=True)
    
    
    # Calculate if the book is currently available
    is_available = fields.Boolean(
        string='Is Available',
        compute='_compute_is_available',
        store=True)
    
    # Compute method to determine availability
    @api.depends('loan_ids.state')
    def _compute_state(self):
        for book in self:
            # Find active loans (ongoing or overdue)
            active_loans = book.loan_ids.filtered(
                lambda l: l.state in ['ongoing', 'overdue']
            )
            
            if active_loans:
                # If any loan is overdue, the book state is overdue
                if any(loan.state == 'overdue' for loan in active_loans):
                    book.state = 'overdue'
                else:
                    book.state = 'loaned'
            else:
                # No active loans, book is available
                book.state = 'available'

    # Method to open loan wizard
    def action_loan_book(self):
        """ Action to loan the book """
        return {
            'name': _('Loan Book'),
            'type': 'ir.actions.act_window',
            'res_model': 'library.loan',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_book_id': self.id,
            },
        }
    
    # Method to search the active loan of the book and set it as returned
    def action_return_book(self):
        """ Action to return the book """
        active_loan = self.loan_ids.filtered(lambda l: l.state in ['ongoing', 'overdue'])
        if active_loan:
            active_loan.write({
                'return_date': fields.Date.context_today(self),
                'state': 'returned'
            })