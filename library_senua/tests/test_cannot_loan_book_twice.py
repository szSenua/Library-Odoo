from datetime import date
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestCannotLoanBookTwice(TransactionCase):
    
    def test_cannot_loan_book_already_loaned(self):

        # Create author and borrower partners
        autor = self.env['res.partner'].create({'name': 'Author'})
        borrower_one = self.env['res.partner'].create({'name': 'Borrower 1'})
        borrower_two = self.env['res.partner'].create({'name': 'Borrower 2'})
        
        # Create a book
        book = self.env['library.book'].create({
            'name': 'Book One',
            'isbn': '123-4567890123',
            'author_id': autor.id,
        })
        
        # First loan
        loan = self.env['library.loan'].create({
            'book_id': book.id,
            'borrower_id': borrower_one.id,
            'loan_date': date.today(),
        })
        
        print(f"\n First loan created: {loan.id} (state: {loan.state})")
        
        # Attempt second loan of the same book - should fail
        with self.assertRaises(ValidationError) as e:
            loan_two = self.env['library.loan'].create({
                'book_id': book.id,
                'borrower_id': borrower_two.id,
                'loan_date': date.today(),
            })
        
        print(f" Error captured: {e.exception}")