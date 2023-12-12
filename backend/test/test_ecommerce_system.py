import unittest
from src.utils.credit_card import CreditCard
from src.utils.month_of_year import MonthOfYear
from src.interfaces.ecommerce_system import EcommerceSystem
from src.ecommerce.active_client import ActiveClient
from src.utils.time import Time
from test.test_doubles.login_system_simulator import LoginSystemSimulator
from test.test_doubles.current_date_and_time_simulator import CurrentDateAndTimeSimulator
from test.test_doubles.payment_processor_simulator import PaymentProcessorSimulator
from src.utils.constants import CATALOGUE_FOR_TESTING

VALID_CREDENTIALS = ("valid client id", "valid password")
INVALID_CREDENTIALS = ("invalid client id", "invalid password")

class TestEcommerceSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.current_time = Time.create_for_exact_datetime(2023, 11, 24, 10, 0, 0)
        self.current_month_of_year = MonthOfYear.with_month_and_year(11, 2023)
        self.current_datetime = CurrentDateAndTimeSimulator.create_with_month_of_year_and_time(self.current_month_of_year, self.current_time)
        self.login_system = LoginSystemSimulator()
        self.ecommerce_system = self._generate_ecommerce_system()
        self.cart_id = self.ecommerce_system.create_cart(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])

    def test01_empty_cart_is_created_correctly(self):
        book_list = self.ecommerce_system.list_cart(self.cart_id)
        self._assert_includes_all_books(book_list, [])
    
    def test02_a_book_is_added_to_a_cart_by_id(self):
        self._add_all_books_to_cart(self.cart_id, ["isbn1"])
        book_list = self.ecommerce_system.list_cart(self.cart_id)
        self._assert_includes_all_books(book_list, ["isbn1"])

    def test03_multiple_books_are_added_to_a_cart_by_id(self):
        self._add_all_books_to_cart(self.cart_id, ["isbn1", "isbn2"])
        book_list = self.ecommerce_system.list_cart(self.cart_id)
        self._assert_includes_all_books(book_list, ["isbn1", "isbn2"])

    def test04_add_to_non_existing_cart_raises_error(self):
        add_book_to_non_existing_cart = lambda: self.ecommerce_system.add_to_cart("non existing cart id", "isbn1", 1)
        self._assert_raises_error(add_book_to_non_existing_cart, ValueError, EcommerceSystem.non_existing_cart_id_error_message())

    def test05_list_non_existing_cart_raises_error(self):
        list_non_existing_cart = lambda: self.ecommerce_system.list_cart("non existing cart id")
        self._assert_raises_error(list_non_existing_cart, ValueError, EcommerceSystem.non_existing_cart_id_error_message())
    
    def test06_creation_of_multiple_carts_have_different_ids(self):
        cart_id_1, cart_id_2 = self._create_multiple_carts(2)
        self.assertNotEqual(cart_id_1, cart_id_2)

    def test07_different_carts_are_listed_with_their_own_books(self):
        cart_id_1, cart_id_2 = self._create_multiple_carts(2)
        self.ecommerce_system.add_to_cart(cart_id_1, "isbn1", 1)
        list_of_books_cart_1, list_of_books_cart_2 = self._list_multiple_carts([cart_id_1, cart_id_2])
        self._assert_includes_all_books(list_of_books_cart_1, ["isbn1"])
        self._assert_includes_all_books(list_of_books_cart_2, [])

    def test08_adding_a_book_with_multiple_copies_has_expected_quantity(self):
        self.ecommerce_system.add_to_cart(self.cart_id, "isbn1", 2)
        book_list = self.ecommerce_system.list_cart(self.cart_id)
        self._assert_includes_all_books(book_list, ["isbn1"])
        self._assert_a_book_quantity(book_list, "isbn1", 2)

    def test09_can_not_create_cart_with_invalid_credentials(self):
        self._add_invalid_credentials_to_login_system()
        create_cart_with_invalid_credentials = lambda: self.ecommerce_system.create_cart(INVALID_CREDENTIALS[0], INVALID_CREDENTIALS[1])
        self._assert_raises_error(create_cart_with_invalid_credentials, ValueError, LoginSystemSimulator.invalid_credentials_error_message())

    def test10_can_not_checkout_cart_with_invalid_card_owner_name(self):
        invalid_owner_name = ""
        checkout_cart_with_invalid_credit_card =  lambda: self.ecommerce_system.checkout_cart(self.cart_id, "123", self.current_month_of_year, invalid_owner_name)
        self._assert_raises_error(checkout_cart_with_invalid_credit_card, ValueError, CreditCard.invalid_card_data_error_message())

    def test11_can_not_checkout_cart_with_empty_card_number(self):
        invalid_credit_card_number = ""
        checkout_cart_with_invalid_credit_card =  lambda: self.ecommerce_system.checkout_cart(self.cart_id, invalid_credit_card_number, self.current_month_of_year, "owner name")
        self._assert_raises_error(checkout_cart_with_invalid_credit_card, ValueError, CreditCard.invalid_card_data_error_message())
    
    def test12_can_not_checkout_cart_with_letters_as_card_number(self):
        invalid_credit_card_number = "abc"
        checkout_cart_with_invalid_credit_card =  lambda: self.ecommerce_system.checkout_cart(self.cart_id, invalid_credit_card_number, self.current_month_of_year, "owner name")
        self._assert_raises_error(checkout_cart_with_invalid_credit_card, ValueError, CreditCard.invalid_card_data_error_message())
    
    def test13_can_not_checkout_non_existing_cart(self):
        non_existing_cart = "non existing cart id"
        checkout_non_existing_cart = lambda: self.ecommerce_system.checkout_cart(non_existing_cart, "123", self.current_month_of_year.one_month_after(), "owner name")
        self._assert_raises_error(checkout_non_existing_cart, ValueError, EcommerceSystem.non_existing_cart_id_error_message())
    
    def test14_checked_out_purchase_is_registered(self):
        self.ecommerce_system.add_to_cart(self.cart_id, "isbn1", 1)
        self.ecommerce_system.checkout_cart(self.cart_id, "123", self.current_month_of_year.one_month_after(), "owner name")
        list_of_purchases = self.ecommerce_system.list_purchases(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])
        self.assertEqual(list_of_purchases[0], 100)
        self.assertEqual(list_of_purchases[1], {"isbn1":1})

    def test15_can_not_add_to_cart_with_expired_session(self):
        add_to_cart_with_expired_session = lambda: self.ecommerce_system.add_to_cart(self.cart_id, "isbn1", 1)
        self._assert_expired_session_fail_for_block(add_to_cart_with_expired_session)

    def test16_can_not_list_cart_with_expired_session(self):
        list_cart_with_expired_session = lambda: self.ecommerce_system.list_cart(self.cart_id)
        self._assert_expired_session_fail_for_block(list_cart_with_expired_session)

    def test17_can_not_checkout_cart_with_expired_session(self):
        checkout_cart_with_expired_session = lambda: self.ecommerce_system.checkout_cart(self.cart_id, "123", self.current_month_of_year, "owner name")
        self._assert_expired_session_fail_for_block(checkout_cart_with_expired_session)

    def test18_cart_session_does_not_expire_if_cart_was_used_adding_a_book(self):
        add_to_cart_with_non_expired_session = lambda: self.ecommerce_system.add_to_cart(self.cart_id, "isbn1", 1)
        self._advance_time_to_not_expired_session(add_to_cart_with_non_expired_session)
        self.ecommerce_system.add_to_cart(self.cart_id, "isbn2", 1)
        self._assert_includes_all_books(self.ecommerce_system.list_cart(self.cart_id), ["isbn1", "isbn2"])

    def test19_cart_session_does_not_expire_if_cart_was_listed(self):
        list_cart_with_non_expired_session = lambda: self.ecommerce_system.list_cart(self.cart_id)
        self._advance_time_to_not_expired_session(list_cart_with_non_expired_session)
        self._assert_includes_all_books(self.ecommerce_system.list_cart(self.cart_id), [])

    def test20_can_not_list_purchases_with_invalid_credentials(self):
        self._add_invalid_credentials_to_login_system()
        list_purchases_with_invalid_credentials = lambda: self.ecommerce_system.list_purchases(INVALID_CREDENTIALS[0], INVALID_CREDENTIALS[1])
        self._assert_raises_error(list_purchases_with_invalid_credentials, ValueError, LoginSystemSimulator.invalid_credentials_error_message())
    
    def test21_purchases_for_different_clients_are_separated(self):
        another_client_id = "other client id"
        another_password = "other password"
        self.ecommerce_system.create_cart(another_client_id, another_password)
        self._add_book_to_cart_and_checkout(self.cart_id, "isbn1", 1)
        list_of_purchases = self.ecommerce_system.list_purchases(another_client_id, another_password)
        self._assert_list_of_purchases_is(list_of_purchases, 0, {})
    
    def test22_checkout_multiple_carts_of_a_client_includes_all_purchases(self):
        self._add_book_to_cart_and_checkout(self.cart_id, "isbn1", 1)
        another_cart_id = self.ecommerce_system.create_cart(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])
        self._add_book_to_cart_and_checkout(another_cart_id, "isbn2", 1)
        list_of_purchases = self.ecommerce_system.list_purchases(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])
        self._assert_list_of_purchases_is(list_of_purchases, 300, {"isbn1":1, "isbn2":1})

    def _generate_ecommerce_system(self):
        payment_processor = PaymentProcessorSimulator()
        return EcommerceSystem.with_login_system_catalogue_datetime_provider_and_payment_processor(self.login_system, CATALOGUE_FOR_TESTING, self.current_datetime, payment_processor)        

    def _create_multiple_carts(self, number_of_carts):
        return [self.ecommerce_system.create_cart(object(), object()) for _ in range(number_of_carts)]

    def _list_multiple_carts(self, cart_ids):
        return [self.ecommerce_system.list_cart(cart_id) for cart_id in cart_ids]

    def _add_all_books_to_cart(self, cart_id, list_of_books_to_add):
        for book in list_of_books_to_add:
            self.ecommerce_system.add_to_cart(cart_id, book, 1)

    def _add_invalid_credentials_to_login_system(self):
        self.login_system.add_invalid_credentials(INVALID_CREDENTIALS[0], INVALID_CREDENTIALS[1])

    def _add_book_to_cart_and_checkout(self, cart_id, book_isbn, quantity):
        self.ecommerce_system.add_to_cart(cart_id, book_isbn, quantity)
        self.ecommerce_system.checkout_cart(cart_id, "123", self.current_month_of_year, "owner name")

    def _assert_a_book_quantity(self, book_list, book, quantity):
        self.assertEqual(book_list[book], quantity)

    def _assert_includes_all_books(self, list_of_existing_books, list_of_books_to_verify):
        self.assertEqual(len(list_of_existing_books), len(list_of_books_to_verify))
        for book in list_of_books_to_verify:
            self.assertIn(book, list_of_existing_books)

    def _assert_expired_session_fail_for_block(self, block_to_fail):
        self.current_datetime.advance_minutes(ActiveClient.expiration_cart_time_in_minutes())
        self._assert_raises_error(block_to_fail, ValueError, ActiveClient.expired_session_error_message())

    def _advance_time_to_not_expired_session(self, block_to_update_session):
        self.current_datetime.advance_minutes(ActiveClient.non_expired_cart_time_in_minutes())
        block_to_update_session()
        self.current_datetime.advance_minutes(ActiveClient.non_expired_cart_time_in_minutes())
    
    def _assert_list_of_purchases_is(self, list_of_purchases, expected_total_price, expected_purchases):
        self.assertEqual(list_of_purchases[0], expected_total_price)
        self.assertEqual(list_of_purchases[1], expected_purchases)

    def _assert_raises_error(self, block_to_fail, error_type, error_message):
        try:
            block_to_fail()
        except error_type as error:
            self.assertEqual(str(error), error_message)
        else:
            self.fail(f"Expected {error_type} but no exception was raised.")

if __name__ == '__main__':
    unittest.main()