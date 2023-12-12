from src.ecommerce.sales_registry import SalesRegistry

class Cashier():
    def __init__ (self, datetime_provider, payment_processor):
        self.datetime_provider = datetime_provider
        self.payment_processor = payment_processor
        self.sales_registry = SalesRegistry()

    @classmethod
    def with_datetime_provider_and_payment_processor(cls, datetime_provider, payment_processor):
        return Cashier(datetime_provider, payment_processor)

    @classmethod
    def checkout_empty_cart_error_message(cls):
        return "Cannot checkout empty cart"

    @classmethod
    def expired_credit_card_error_message(cls):
        return "Cannot checkout with expired credit card"

    @classmethod
    def unable_to_process_payment_error_message(cls):
        return "Unable to process payment"
    
    def checkout_cart(self, client_id, cart, credit_card):
        self._validate_cart_is_not_empty(cart)
        self._validate_credit_card_is_not_expired(credit_card)
        total_price_of_sale = cart.total_price()
        self._process_payment(total_price_of_sale, credit_card)
        return self.sales_registry.register_sale(client_id, total_price_of_sale, cart.books())
    
    def sales_for_client(self, client_id):
        return self.sales_registry.sales_summary_for_client(client_id)
    
    def _validate_cart_is_not_empty(self, cart):
        if (cart.is_empty()):
            raise ValueError(self.checkout_empty_cart_error_message())

    def _validate_credit_card_is_not_expired(self, credit_card):
        current_month_of_year = self.datetime_provider.current_month_of_year()
        if (credit_card.is_expired(current_month_of_year)):
            raise ValueError(self.expired_credit_card_error_message())
    
    def _process_payment(self, price_to_charge, credit_card):
        try:
            self.payment_processor.process_payment(price_to_charge, credit_card)
        except:
            raise ValueError(self.unable_to_process_payment_error_message())
    
