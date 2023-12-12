class Sale():
    def __init__(self, total_price, sold_books):
        self.total_price = total_price
        self.sold_books = sold_books

    @classmethod
    def with_total_price_and_books(cls, total_price, sold_books):
        return Sale(total_price, sold_books)

    def price(self):
        return self.total_price
    
    def books(self):
        return self.sold_books
    