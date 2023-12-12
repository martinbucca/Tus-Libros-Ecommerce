import unittest
from src.ecommerce.cart import Cart
from src.utils.constants import CATALOGUE_WITH_NAMED_BOOKS_FOR_TESTING

class TestCart(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = Cart.with_books_catalogue(CATALOGUE_WITH_NAMED_BOOKS_FOR_TESTING)

    def test01_new_cart_is_empty(self):
        self.assertTrue(self.cart.is_empty())

    def test02_one_book_is_added_to_the_cart_correctly(self):
        self._add_all_books_to_cart(["Modern Software Engineering"])
        self.assertFalse(self.cart.is_empty())
        self._assert_includes_books(["Modern Software Engineering"])

    def test03_multiple_books_are_added_to_the_cart_correctly(self):
        self._add_all_books_to_cart(["Modern Software Engineering", "Extreme Programming Explained"])
        self.assertTrue(self.cart.has_quantity(2))
        self._assert_includes_books(["Modern Software Engineering", "Extreme Programming Explained"])

    def test04_a_book_not_included_in_catalogue_cannot_be_added_to_the_cart(self):
        add_non_existing_book_to_cart = lambda: self.cart.add_book("Non existing book", 1)
        self._assert_raises_error_and_cart_is_empty(add_non_existing_book_to_cart, ValueError, Cart.book_not_in_catalogue_error_message())
    
    def test05_more_than_one_copy_of_a_book_can_be_added_to_the_cart(self):
        self.cart.add_book("Modern Software Engineering", 2)
        self.assertTrue(self.cart.has_quantity(2))
        self.assertTrue(self.cart.has_book("Modern Software Engineering", 2))
    
    def test06_a_book_with_invalid_quantity_cannot_be_added_to_the_cart(self):
        add_book_with_invalid_quantity_to_cart = lambda: self.cart.add_book("Modern Software Engineering", 0)
        self._assert_raises_error_and_cart_is_empty(add_book_with_invalid_quantity_to_cart, ValueError, Cart.book_quantity_error_message())

    def _add_all_books_to_cart(self, list_of_books_to_add):
        for book in list_of_books_to_add:
            self.cart.add_book(book, 1)

    def _assert_includes_books(self, list_of_books):
        for book in list_of_books:
            self.assertTrue(self.cart.has_book(book, 1))
    
    def _assert_raises_error_and_cart_is_empty(self, block_to_fail, error_type, error_message):
        try:
            block_to_fail()
        except error_type as error_raised:
            self.assertEqual(str(error_raised), error_message)
            self.assertTrue(self.cart.is_empty())
        else:
            self.fail(f"Expected {error_type} but no exception was raised.")

if __name__ == '__main__':
    unittest.main()