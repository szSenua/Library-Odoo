from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

# Test to ensure ISBN uniqueness in library.book model
class TestIsbnUniqueness(TransactionCase):
    
    def test_isbn_unique(self):
        autor = self.env['res.partner'].create({'name': 'Test Author'})
        
        # Creates first book
        self.env['library.book'].create({
            'name': 'Book One',
            'isbn': '123-4567890123',
            'author_id': autor.id,
        })
        
        print("Trying to duplicate ISBN...")
        
        # Attempt to duplicate
        try:
            self.env['library.book'].create({
                'name': 'Book Two',
                'isbn': '123-4567890123',
                'author_id': autor.id,
            })
            print("FAIL: Duplicate was created")
            self.fail("Should not create book with duplicate ISBN")
            
        except ValidationError as e:
            print(f"OK: {e}")