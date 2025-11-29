from odoo import models, fields, api, _

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
