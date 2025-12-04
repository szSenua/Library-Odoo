from odoo.tests.common import TransactionCase

class TestSearchByAuthor(TransactionCase):
    
    def test_search_by_author(self):
        
        # Create author and borrower partners
        author = self.env['res.partner'].create({'name': 'Author A'})
        borrower = self.env['res.partner'].create({'name': 'Borrower A'})
        
        # Create books
        book = self.env['library.book'].create({
            'name': 'Book One',
            'isbn': '111-1111111111',
            'author_id': author.id,
        })
        book_two = self.env['library.book'].create({
            'name': 'Book Two',
            'isbn': '222-2222222222',
            'author_id': author.id,
        })
        
        # Create loans for the books
        loan_one = self.env['library.loan'].create({
            'book_id': book.id,
            'borrower_id': borrower.id,
        })
        loan_two = self.env['library.loan'].create({
            'book_id': book_two.id,
            'borrower_id': borrower.id,
        })
        
        # Search for loans by author
        loans_by_author = self.env['library.loan'].search([('book_id.author_id', '=', author.id)])
        
        print(f"\n Loans found for author '{author.name}': {[loan.id for loan in loans_by_author]}")
        
        # Verify that both loans are found
        self.assertEqual(len(loans_by_author), 2, f"Expected 2 loans for author '{author.name}', found {len(loans_by_author)}")
        self.assertIn(loan_one, loans_by_author, "Loan 1 not found in search results")
        self.assertIn(loan_two, loans_by_author, "Loan 2 not found in search results")
        
        print(" Test passed!")