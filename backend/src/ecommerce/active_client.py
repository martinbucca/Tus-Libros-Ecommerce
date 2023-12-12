class ActiveClient():
    def __init__(self, cart, datetime_provider) -> None:
        self.cart = cart
        self.datetime_provider = datetime_provider
        self.last_used_cart_time = datetime_provider.current_time()

    @classmethod
    def create_with_cart_and_datetime_provider(cls, cart, datetime_provider):
        return ActiveClient(cart, datetime_provider)

    @classmethod
    def expired_session_error_message(cls):
        return "Session expired"
    
    @classmethod
    def expiration_cart_time_in_minutes(cls):
        return 30
    
    @classmethod
    def non_expired_cart_time_in_minutes(cls):
        return 20

    def books_in_cart(self):
        self._handle_cart_expiration()
        return self.cart.books()

    def add_to_cart(self, isbn, quantity):
        self._handle_cart_expiration()
        self.cart.add_book(isbn, quantity)

    def cart_for_checkout(self):
        self._handle_cart_expiration()
        return self.cart
    
    def _handle_cart_expiration(self):
        self._assert_cart_is_not_expired()
        self._update_last_time_used_cart()

    def _assert_cart_is_not_expired(self):
        current_time = self.datetime_provider.current_time()
        creation_time = self.last_used_cart_time
        if (current_time.passed_minutes(creation_time, self.expiration_cart_time_in_minutes())):
            raise ValueError(self.expired_session_error_message())

    def _update_last_time_used_cart(self):
        self.last_used_cart_time  = self.datetime_provider.current_time()