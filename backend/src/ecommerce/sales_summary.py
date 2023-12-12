from collections import Counter

class SalesSummary():
    def __init__(self, total_price_of_sales, sold_books):
        self.price_of_sales = total_price_of_sales
        self.sold_books = sold_books
    
    @classmethod
    def generate_from_sales(cls, sales):
        total_price_of_sales = 0
        sold_books = Counter()
        for sale in sales:
            total_price_of_sales += sale.price()
            sold_books += sale.books()
        return cls(total_price_of_sales, sold_books)
    
    def total_price_of_sales(self):
        return self.price_of_sales
    
    def books(self):
        return dict(self.sold_books)