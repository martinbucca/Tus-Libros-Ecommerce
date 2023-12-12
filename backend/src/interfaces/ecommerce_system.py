from src.utils.credit_card import CreditCard
from src.ecommerce.cart import Cart
from src.ecommerce.cashier import Cashier
from src.utils.id import Id
from src.ecommerce.active_client import ActiveClient
class EcommerceSystem():
    def __init__(self, loginSystem, catalogue, datetime_provider, payment_processor) -> None:
        self.login_system = loginSystem
        self.catalogue = catalogue
        self.datetime_provider = datetime_provider
        self.cashier = Cashier.with_datetime_provider_and_payment_processor(datetime_provider, payment_processor)
        self.cart_id_for_client_id = {} 
        self.active_clients = {} 

    @classmethod
    def with_login_system_catalogue_datetime_provider_and_payment_processor(cls, login_system, catalogue, datetime_provider, payment_processor):
        return EcommerceSystem(login_system, catalogue, datetime_provider, payment_processor)

    @classmethod
    def non_existing_cart_id_error_message(cls):
        return "Cart id does not exist"

    def create_cart(self, client_id, password):
        self.login_system.authenticate_client_id_and_password(client_id, password)
        cart_id, cart_for_client = self._create_cart_for_client(client_id)
        self.active_clients[client_id] = ActiveClient.create_with_cart_and_datetime_provider(cart_for_client, self.datetime_provider)
        return cart_id
    
    def list_cart(self, cart_id):
        active_client = self._active_client_for_cart_id(cart_id)
        return active_client.books_in_cart()
        
    def add_to_cart(self, cart_id, isbn, quantity):
        active_client = self._active_client_for_cart_id(cart_id)
        active_client.add_to_cart(isbn, quantity)
        
    def checkout_cart(self, cart_id, credit_card_number, expiration_date, owner_name):
        client_id = self._client_id_for_cart_id(cart_id)
        cart_of_client = self._cart_for_checkout(cart_id)
        creadit_card = CreditCard.with_credit_card_number_expiration_month_of_year_and_owner(credit_card_number, expiration_date, owner_name)
        return self.cashier.checkout_cart(client_id, cart_of_client, creadit_card)
    
    def list_purchases(self, client_id, password):
        self.login_system.authenticate_client_id_and_password(client_id, password)
        sales_summary = self.cashier.sales_for_client(client_id)
        return (sales_summary.total_price_of_sales(), sales_summary.books())


    def _assert_cart_id_exists(self, cart_id):
        if (cart_id not in self.cart_id_for_client_id):
            raise ValueError(self.non_existing_cart_id_error_message())

    def _client_id_for_cart_id(self, cart_id):
        self._assert_cart_id_exists(cart_id)
        return self.cart_id_for_client_id[cart_id]

    def _active_client_for_cart_id(self, cart_id):
        client_id = self._client_id_for_cart_id(cart_id)
        return self.active_clients[client_id]

    def _create_cart_for_client(self, client_id):
        cart_id = Id.generate()
        cart = Cart.with_books_catalogue(self.catalogue)
        self.cart_id_for_client_id[cart_id] = client_id
        return cart_id, cart

    def _cart_for_checkout(self, cart_id):
        active_client = self._active_client_for_cart_id(cart_id)
        return active_client.cart_for_checkout()


    
    