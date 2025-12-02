from odoo import fields
from datetime import date, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

# Test return late functionality in library.book model
class TestReturnLate(TransactionCase):
    
    def test_return_late(self):

        # Create author and borrower partners
        autor = self.env['res.partner'].create({'name': 'Author'})
        borrower = self.env['res.partner'].create({'name': 'Borrower'})
        
        # Create a book
        book = self.env['library.book'].create({
            'name': 'Book One',
            'isbn': '123-4567890123',
            'author_id': autor.id,
        })
        
        # Loan made 10 days ago
        loan = self.env['library.loan'].create({
            'book_id': book.id,
            'borrower_id': borrower.id,
            'loan_date': date.today() - timedelta(days=10),
        })

        # Force recomputation of computed fields
        loan._compute_is_late()
        loan._compute_state()
        
        print(f"\n VALUES:")
        print(f"   is_late: {loan.is_late} (expected: True)")
        print(f"   days_late: {loan.days_late} (expected: 5)")
        print(f"   state: {loan.state} (expected: overdue)")
        
        self.assertTrue(loan.is_late, f" is_late es {loan.is_late}, expected True")
        self.assertEqual(loan.state, 'overdue', f" state es '{loan.state}', expected 'overdue'")
        self.assertEqual(loan.days_late, 5, f" days_late es {loan.days_late}, expected 5")
        
        # Return the book today
        loan.return_date = date.today()
        loan._compute_is_late()
        loan._compute_state()
        
        print(f"\n  AFTER RETURN:")
        print(f"   state: {loan.state} (expected: returned)")
        print(f"   days_late: {loan.days_late} (expected: 5)")
        
        # Verify
        self.assertEqual(loan.state, 'returned', f" state es '{loan.state}', expected 'returned'")
        self.assertEqual(loan.days_late, 5, f" days_late es {loan.days_late}, expected 5")
        
        print("  Test passed!")