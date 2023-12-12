from collections import Counter

class Cart():
    def __init__(self, books_catalogue) -> None:
        self.added_books = Counter()
        self.catalogue = books_catalogue
    
    @classmethod
    def with_books_catalogue(cls, books_catalogue):
        return Cart(books_catalogue)

    @classmethod
    def book_not_in_catalogue_error_message(cls):
        return "Book not found"
    
    @classmethod
    def book_quantity_error_message(cls):
        return "Must add at least one book"
    
    def is_empty(self):
        return (len(self.added_books) == 0)
    
    def add_book(self, book, quantity):
        self._assert_can_add_book(book, quantity)
        self.added_books[book] += quantity

    def has_quantity(self, quantity):
        return self.added_books.total()
    
    def has_book(self, book, quantity):
        return self.added_books[book] == quantity
    
    def books(self):
        return self.added_books.copy()
    
    def total_price(self):
        return sum([self._price_of_book(book) for book in self.added_books.elements()])

    def _price_of_book(self, book):
        return self.catalogue[book]
    
    def _assert_can_add_book(self, book, quantity):
        self._assert_book_quantity_is_valid(quantity)
        self._assert_book_in_catalogue(book)
    
    def _assert_book_quantity_is_valid(self, quantity):
        if (quantity < 1):
            raise ValueError(Cart.book_quantity_error_message())

    def _assert_book_in_catalogue(self, book):
        if (book not in self.catalogue):
            raise ValueError(Cart.book_not_in_catalogue_error_message())
    
        