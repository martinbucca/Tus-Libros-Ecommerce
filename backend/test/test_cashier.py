import unittest
from src.ecommerce.cart import Cart
from src.ecommerce.cashier import Cashier
from src.utils.credit_card import CreditCard
from src.utils.month_of_year import MonthOfYear
from test.test_doubles.current_date_and_time_simulator import CurrentDateAndTimeSimulator
from test.test_doubles.payment_processor_simulator import PaymentProcessorSimulator
from src.utils.constants import CATALOGUE_WITH_NAMED_BOOKS_FOR_TESTING

class TestCashier(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_client_id = "a client id"
        self.current_month_of_year = MonthOfYear.with_month_and_year(11, 2023)
        self.cashier = self._generate_cashier_with_simulated_current_datetime(self.current_month_of_year)
        self.cart = Cart.with_books_catalogue(CATALOGUE_WITH_NAMED_BOOKS_FOR_TESTING)
        self.valid_credit_card = self._generate_credit_card_with_month_of_year(self.current_month_of_year.one_month_after())

    def test01_can_not_checkout_empty_cart(self):
        checkout_empty_cart = lambda: self.cashier.checkout_cart(object(), self.cart, self.valid_credit_card)
        self._assert_raises_error(checkout_empty_cart, ValueError, Cashier.checkout_empty_cart_error_message())
    
    def test02_can_not_checkout_with_expired_credit_card(self):
        self.cart.add_book("Modern Software Engineering", 1)
        expired_credit_card = self._generate_credit_card_with_month_of_year(self.current_month_of_year.one_month_before())
        checkout_with_expired_cart = lambda: self.cashier.checkout_cart(object(), self.cart, expired_credit_card)
        self._assert_raises_error(checkout_with_expired_cart, ValueError, Cashier.expired_credit_card_error_message())
    
    def test03_cashier_does_not_have_registered_sale_for_client_without_purchases(self):
        sales_summary = self.cashier.sales_for_client(self.valid_client_id)
        self._assert_summary_is_for_price_and_books(sales_summary, 0, {})
    
    def test04_cashier_has_registered_sale_for_a_client(self):
        self.cart.add_book("Modern Software Engineering", 1)
        self.cashier.checkout_cart(self.valid_client_id, self.cart, self.valid_credit_card)
        self._generate_sales_summary_and_assert_is_for_price_and_books(self.valid_client_id, 31505, {"Modern Software Engineering": 1})
        
    def test05_cashier_has_registered_sales_from_different_carts_of_same_client(self):
        self._add_book_and_checkout(self.valid_client_id, self.cart, "Modern Software Engineering", 1)
        another_client_id = "another client id"
        other_cart = Cart.with_books_catalogue(CATALOGUE_WITH_NAMED_BOOKS_FOR_TESTING)
        self._add_book_and_checkout(another_client_id, other_cart, "Extreme Programming Explained", 1)
        self._generate_sales_summary_and_assert_is_for_price_and_books(self.valid_client_id, 31505, {"Modern Software Engineering": 1})
        self._generate_sales_summary_and_assert_is_for_price_and_books(another_client_id, 45305, {"Extreme Programming Explained": 1})
    
    def test06_payment_processor_error_does_not_register_sale_for_a_client(self):
        payment_processor_to_fail = PaymentProcessorSimulator.with_behaviour_to_fail()
        cashier = self._generate_cashier_with_simulated_current_datetime_with_payment_processor(self.current_month_of_year, payment_processor_to_fail)
        self.cart.add_book("Modern Software Engineering", 1)
        purchase_to_fail = lambda: cashier.checkout_cart(self.valid_client_id, self.cart, self.valid_credit_card)
        self._assert_raises_error(purchase_to_fail, ValueError, Cashier.unable_to_process_payment_error_message())
        self._generate_sales_summary_and_assert_is_for_price_and_books(self.valid_client_id, 0, {})
        self.assertFalse(payment_processor_to_fail.has_processed_payment())

    def _assert_raises_error(self, block_to_fail, error_type, error_message):
        try:
            block_to_fail()
        except error_type as error_raised:
            self.assertEqual(str(error_raised), error_message)
        else:
            self.fail(f"Expected {error_type} but no exception was raised.")

    def _generate_credit_card_with_month_of_year (self, month_of_year):
        return CreditCard.with_credit_card_number_expiration_month_of_year_and_owner("123456789", month_of_year, "An owner name")
    
    def _generate_cashier_with_simulated_current_datetime(self, month_of_year):
        payment_processor = PaymentProcessorSimulator.with_behaviour_to_succeed()
        return self._generate_cashier_with_simulated_current_datetime_with_payment_processor(month_of_year, payment_processor)

    def _generate_cashier_with_simulated_current_datetime_with_payment_processor(self, month_of_year, payment_processor):
        simulated_current_datetime = CurrentDateAndTimeSimulator.create_with_month_of_year(month_of_year)
        return Cashier.with_datetime_provider_and_payment_processor(simulated_current_datetime, payment_processor)
    
    def _add_book_and_checkout(self, client_id, cart, book_isbn, quantity):
        cart.add_book(book_isbn, quantity)
        self.cashier.checkout_cart(client_id, cart, self.valid_credit_card)
    
    def _generate_sales_summary_and_assert_is_for_price_and_books(self, client_id, total_price, books):
        sales_summary = self.cashier.sales_for_client(client_id)
        self._assert_summary_is_for_price_and_books(sales_summary, total_price, books)

    def _assert_summary_is_for_price_and_books(self, sales_summary, total_price, books):
        self.assertEqual(sales_summary.total_price_of_sales(), total_price)
        self.assertEqual(sales_summary.books(), books)


if __name__ == '__main__':
    unittest.main()