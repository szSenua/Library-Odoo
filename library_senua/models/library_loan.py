from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Computed name field
    name = fields.Char(
        string='Loan Reference',
        compute='_compute_name',
        store=True,
    )
    
    @api.depends('book_id', 'borrower_id', 'loan_date')
    # Method to compute the name of the loan record
    def _compute_name(self):
        for loan in self:
            # Construct the name as "Book Name - Borrower Name
            if loan.book_id and loan.borrower_id:
                loan.name = f"{loan.book_id.name} - {loan.borrower_id.name}"
            else:
                # Fallback name if book or borrower is missing
                loan.name = f"Loan {loan.id or 'New'}"

    # Book being loaned
    book_id = fields.Many2one('library.book', string='Book', required=True)
    # Borrower of the book
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    # You create a new loan, so the default is today's date
    loan_date = fields.Date(string='Loan Date', default=fields.Date.context_today, required=True)
    # Expected return date
    return_date = fields.Date(string='Return Date')
    # Loan status
    state = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
        ], string='Status', compute='_compute_state', store=True, readonly=False)
    
    # ISBN field
    book_isbn = fields.Char(
        related='book_id.isbn',
        string='ISBN',
        readonly=True,
        store=True
        )
    
    # Compute method to determine loan state
    @api.depends('loan_date', 'return_date', 'is_late')
    def _compute_state(self):
        for loan in self:
            if loan.return_date:
                loan.state = 'returned'
            elif loan.is_late:
                loan.state = 'overdue'
            else:
                loan.state = 'ongoing'

    # Additional notes about the loan
    notes = fields.Text(string='Notes')
    # is_late computed field
    is_late = fields.Boolean(
        string='Is Late',
        compute='_compute_is_late',
        store=True)
    
    # days_late computed field
    days_late = fields.Integer(
        string='Days Late',
        compute='_compute_is_late',  # ← Cambio: usar el mismo método
        store=True)
    
    # Compute method to determine if the loan is late
    @api.depends('loan_date', 'return_date', 'state')
    def _compute_is_late(self):
        for loan in self:
            if loan.return_date and loan.loan_date:
                # Calculate days between loan and return
                delta = (loan.return_date - loan.loan_date).days
            
                if delta > 5:
                    loan.is_late = True
                    loan.days_late = delta - 5
                else:
                    loan.is_late = False
                    loan.days_late = 0
            else:
                # Not yet returned
                if loan.state == 'ongoing' and loan.loan_date:
                    # Calculate days from loan date to today
                    today = fields.Date.context_today(loan)
                    delta = (today - loan.loan_date).days
                
                    if delta > 5:
                        loan.is_late = True
                        loan.days_late = delta - 5
                        # Change state to overdue (not yet returned)
                        loan.state = 'overdue'
                    else:
                        loan.is_late = False
                        loan.days_late = 0
                else:
                    loan.is_late = False
                    loan.days_late = 0
    
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