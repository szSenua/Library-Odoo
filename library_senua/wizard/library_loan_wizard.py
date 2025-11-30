from odoo import _, fields, models
from odoo.exceptions import ValidationError

class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'
    _description = 'Library Loan Wizard'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)

    loan_date = fields.Date(string='Loan Date', default=fields.Date.context_today, required=True)

    notes = fields.Text(string='Notes')

    book_isbn = fields.Char(
        related='book_id.isbn',
        string='ISBN',
        readonly=True
)

    def action_confirm_loan(self):
        # Create a new loan record
        self.env['library.loan'].create({
            'book_id': self.book_id.id,
            'borrower_id': self.borrower_id.id,
            'loan_date': self.loan_date,
            'notes': self.notes,
            'state': 'ongoing'
        })
        
        return {'type': 'ir.actions.act_window_close'}