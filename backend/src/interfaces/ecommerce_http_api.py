from src.utils.month_of_year import MonthOfYear
from src.interfaces.interface_protocol import Response
from src.utils.id import Id

def request_handler(block_to_run):
    def handler(self, request_to_handle):
        try:
            return block_to_run(self, request_to_handle)
        except (ValueError, RuntimeError) as error:
            return Response.generate_error_response_with(error)
    return handler

class EcommerceHttpAPI():
    def __init__(self, ecommerce_system) -> None:
        self.ecommerce_system = ecommerce_system

    @classmethod
    def with_ecommerce_system(cls, ecommerce_system):
        return EcommerceHttpAPI(ecommerce_system)

    @classmethod
    def invalid_cart_id_error_message(cls):
        return "Cart id is invalid"
    
    @classmethod
    def invalid_expiration_date_card_error_message(cls):
        return "Card Expiration date is invalid"
    
    @classmethod
    def invalid_book_quantity_error_message(cls):
        return "Book quantity is invalid"

    @request_handler
    def request_create_cart(self, request):
        client_id_from_request = request.body['clientId']
        password_from_request = request.body['password']
        cart_id = self.ecommerce_system.create_cart(client_id_from_request, password_from_request)
        return Response.generate_success_response_with(cart_id)

    @request_handler
    def request_add_to_cart(self, request):
        cart_id_from_request = request.body['cartId']
        quantity_of_copies = self._string_to_book_quantity(request.body['bookQuantity'])
        book_isbn = request.body["bookIsbn"]
        cart_id = self._string_to_cart_id(cart_id_from_request)
        self.ecommerce_system.add_to_cart(cart_id, book_isbn, quantity_of_copies)
        return Response.generate_success_response_with("OK")

    @request_handler       
    def request_list_cart(self, request):
        cart_id_from_request = request.body['cartId']
        cart_id = self._string_to_cart_id(cart_id_from_request)
        book_list = self.ecommerce_system.list_cart(cart_id)
        book_list_string = self._book_list_to_string(book_list)
        return Response.generate_success_response_with(book_list_string)
        
    @request_handler
    def request_checkout_cart(self, request):
        cart_id_from_request = request.body['cartId']
        credit_card_number = request.body['ccn']
        expiration_month_of_year_as_string = request.body['cced']
        owner_name = request.body['cco']
        cart_id = self._string_to_cart_id(cart_id_from_request)
        expiration_month_of_year = self._string_to_expiration_month_of_year(expiration_month_of_year_as_string)
        transaction_id = self.ecommerce_system.checkout_cart(cart_id, credit_card_number, expiration_month_of_year, owner_name)
        return Response.generate_success_response_with(transaction_id)
    
    @request_handler
    def request_list_purchases(self, request):
        client_id = request.body['clientId']
        password = request.body['password']
        purchases = self.ecommerce_system.list_purchases(client_id, password)
        purchases_string = self._purchases_to_string(purchases)
        return Response.generate_success_response_with(purchases_string)
    

    def _string_to_expiration_month_of_year(self, expiration_month_of_year_as_string):
        try: 
            return MonthOfYear.create_from_string(expiration_month_of_year_as_string)
        except:
            raise ValueError(EcommerceHttpAPI.invalid_expiration_date_card_error_message())
        
    def _string_to_cart_id(self, cart_id_to_convert):
        try:
            return Id.create_from_string(cart_id_to_convert)
        except:
            raise ValueError(EcommerceHttpAPI.invalid_cart_id_error_message())
        
    def _string_to_book_quantity(self, book_quantity_to_convert):
        try:
            return int(book_quantity_to_convert)
        except:
            raise ValueError(EcommerceHttpAPI.invalid_book_quantity_error_message())

    def _book_list_to_string(self, book_list):
        book_list_string = "|".join([f"{book}|{quantity}" for book, quantity in book_list.items()])
        return book_list_string
    
    def _purchases_to_string(self, purchases):
        total_price, books_purchased = purchases
        if (len(books_purchased) == 0):
            return f"{total_price}"
        purchases_string = "|".join([f"{book}|{quantity}" for book, quantity in books_purchased.items()])
        purchases_string = f"{purchases_string}|{total_price}"
        return purchases_string
    
