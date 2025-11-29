from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    # You create a new loan, so the default is today's date
    loan_date = fields.Date(string='Loan Date', default=fields.Date.context_today, required=True)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ], string='Status', default='ongoing', required=True)
    notes = fields.Text(string='Notes')

    # Constraint to prevent loaning a book that is already on loan
    @api.constrains('book_id', 'state')
    def _check_book_availability(self):
        # Only check for ongoing loans
        for loan in self:
            # Check if the loan is ongoing
            if loan.state == 'ongoing':
                # Look for other ongoing loans for the same book
                ongoing_loans = self.search([
                    ('book_id', '=', loan.book_id.id),
                    ('state', '=', 'ongoing'),
                    ('id', '!=', loan.id)
                ])
                # If there are any, raise a validation error
                if ongoing_loans:
                    raise ValidationError(_("This book is already on loan."))
                
                