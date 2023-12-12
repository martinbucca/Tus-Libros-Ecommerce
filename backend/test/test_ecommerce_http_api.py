import unittest
from src.ecommerce.cashier import Cashier
from src.interfaces.ecommerce_http_api import EcommerceHttpAPI
from src.interfaces.ecommerce_system import EcommerceSystem
from src.interfaces.interface_protocol import Request, Response
from test.test_doubles.login_system_simulator import LoginSystemSimulator
from test.test_doubles.current_date_and_time_simulator import CurrentDateAndTimeSimulator
from test.test_doubles.payment_processor_simulator import PaymentProcessorSimulator
from src.utils.id import Id
from src.utils.time import Time
from src.utils.month_of_year import MonthOfYear
from src.utils.constants import CATALOGUE_FOR_TESTING

VALID_CREDENTIALS = ("valid client id", "valid password")
INVALID_CREDENTIALS = ("invalid client id", "invalid password")

class TestEcommerceHttpAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.current_time = Time.create_for_exact_datetime(2023, 11, 24, 10, 0, 0)
        self.current_month_of_year = MonthOfYear.with_month_and_year(11, 2023)
        self.current_datetime = CurrentDateAndTimeSimulator.create_with_month_of_year_and_time(self.current_month_of_year, self.current_time)
        self.login_system = LoginSystemSimulator()
        self.ecommerce_http_api = self._generate_ecommerce_http_api()
        self.cart_id = self._create_cart(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])

    @classmethod
    def expected_success_body_code(cls):
        return "0"
    @classmethod
    def expected_error_body_code(cls):
        return "1"
    @classmethod
    def expected_body_separator(self):
        return "|"
    @classmethod
    def expected_success_status_code(self):
        return 200
    @classmethod
    def expected_error_status_code(self):
        return 200

    def test01_create_cart_response_is_correctly_serialized(self):
        request_create_cart = Request.create_with_body({"clientId":VALID_CREDENTIALS[0], "password":VALID_CREDENTIALS[1]})
        response_create_cart = self.ecommerce_http_api.request_create_cart(request_create_cart)
        self._assert_is_id_success_reponse(response_create_cart)

    def test02_add_to_cart_with_no_error_response_is_correctly_serialized(self):
        response_add_to_cart = self._add_to_cart(self.cart_id, "isbn1", 1)
        self._assert_succes_response(response_add_to_cart, "OK")

    def test03_list_cart_on_empty_cart_is_correctly_serialized(self):
        response_list_cart = self._list_cart(self.cart_id)
        self._assert_succes_response(response_list_cart, "")

    def test04_list_cart_includes_added_book_in_response(self):
        self._add_to_cart(self.cart_id, "isbn1", 1)
        response_list_cart = self._list_cart(self.cart_id)
        self._assert_succes_response(response_list_cart, "isbn1|1")

    def test05_list_cart_includes_multiple_added_books_in_response(self):
        self._add_to_cart(self.cart_id, "isbn1", 1)
        self._add_to_cart(self.cart_id, "isbn2", 1)
        response_list_cart = self._list_cart(self.cart_id)
        self._assert_succes_response(response_list_cart, "isbn1|1|isbn2|1")

    def test06_add_to_cart_error_is_correctly_serialized(self):
        invalid_cart_id = Id.create_as_string()
        response_add_to_cart = self._add_to_cart(invalid_cart_id, "isbn1", 1)
        self._assert_error_response(response_add_to_cart, EcommerceSystem.non_existing_cart_id_error_message())

    def test07_list_cart_error_is_correctly_serialized(self):
        invalid_cart_id = Id.create_as_string()
        response_list_cart = self._list_cart(invalid_cart_id)
        self._assert_error_response(response_list_cart, EcommerceSystem.non_existing_cart_id_error_message())

    def test08_invalid_cart_id_error_is_correctly_serialized(self):
        response_add_to_cart = self._add_to_cart("0", "isbn1", 1)
        self._assert_error_response(response_add_to_cart, EcommerceHttpAPI.invalid_cart_id_error_message())
    
    def test09_add_multiple_copies_ok_response_is_correctly_serialized(self):
        response_add_to_cart = self._add_to_cart(self.cart_id, "isbn1", 2)
        self._assert_succes_response(response_add_to_cart, "OK")
    
    def test10_list_cart_with_multiple_copies_of_a_book_is_correctly_serialized(self):
        self._add_to_cart(self.cart_id, "isbn1", 2)
        response_list_cart = self._list_cart(self.cart_id)
        self._assert_succes_response(response_list_cart, "isbn1|2")
    
    def test11_create_cart_with_invalid_credentials_error_is_correctly_serialized(self):
        self._add_invalid_credentials_to_login_system()
        request_create_cart = Request.create_with_body({"clientId":INVALID_CREDENTIALS[0], "password":INVALID_CREDENTIALS[1]})
        response_create_cart = self.ecommerce_http_api.request_create_cart(request_create_cart)
        self._assert_error_response(response_create_cart, LoginSystemSimulator.invalid_credentials_error_message())

    def test12_checkout_with_non_existing_cart_id_error_is_correctly_serialized(self):
        non_existing_cart_id = Id.create_as_string()
        response_checkout_cart = self._checkout_cart(non_existing_cart_id, "123455", "112023", "Owner Name")
        self._assert_error_response(response_checkout_cart, EcommerceSystem.non_existing_cart_id_error_message())

    def test13_checkout_empty_cart_error_is_correctly_serialized(self):
        response_checkout_cart = self._checkout_cart(self.cart_id, "123455", "112024", "Owner Name")
        self._assert_error_response(response_checkout_cart, Cashier.checkout_empty_cart_error_message())

    def test14_checkout_with_invalid_expiration_date_error_is_correctly_serialized(self):
        response_checkout_cart = self._checkout_cart(self.cart_id, "123455", "1120", "Owner Name")
        self._assert_error_response(response_checkout_cart, EcommerceHttpAPI.invalid_expiration_date_card_error_message())

    def test15_succesfull_checkout_cart_is_correctly_serialized(self):
        response_checkout_cart = self._add_to_cart_and_checkout(self.cart_id, "isbn1", 1)
        self._assert_is_id_success_reponse(response_checkout_cart)

    def test16_list_purchases_with_invalid_credentials_error_is_correctly_serialized(self):
        self._add_invalid_credentials_to_login_system()
        request_list_purchases = Request.create_with_body({"clientId":INVALID_CREDENTIALS[0], "password":INVALID_CREDENTIALS[1]})
        response_list_purchases = self.ecommerce_http_api.request_list_purchases(request_list_purchases)
        self._assert_error_response(response_list_purchases, LoginSystemSimulator.invalid_credentials_error_message())
    
    def test17_list_purchases_for_client_without_purchases_is_correctly_serialized(self):
        response_list_purchases = self._list_purchases(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])
        self._assert_succes_response(response_list_purchases, "0")

    def test18_list_multiple_purchases_is_correctly_serialized(self):
        self._add_to_cart_and_checkout(self.cart_id, "isbn1", 1)
        other_cart_id = self._create_cart(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])
        self._add_to_cart_and_checkout(other_cart_id, "isbn2", 1)
        response_list_purchases = self._list_purchases(VALID_CREDENTIALS[0], VALID_CREDENTIALS[1])
        self._assert_succes_response(response_list_purchases, "isbn1|1|isbn2|1|300")


    def _generate_ecommerce_http_api(self):
        payment_processor = PaymentProcessorSimulator()
        ecommerce_system = EcommerceSystem.with_login_system_catalogue_datetime_provider_and_payment_processor(self.login_system, CATALOGUE_FOR_TESTING, self.current_datetime, payment_processor)
        return EcommerceHttpAPI.with_ecommerce_system(ecommerce_system)

    def _create_cart(self, client_id, password):
        body = {"clientId":client_id, "password":password}
        request_create_cart = Request.create_with_body(body)
        response_create_cart = self.ecommerce_http_api.request_create_cart(request_create_cart)
        cart_id = self._cart_id(response_create_cart)
        return cart_id
    
    def _cart_id(self, response):
        body = response.body
        return body.split(self.expected_body_separator())[-1]

    def _add_to_cart(self, cart_id, book_isbn, quantity):
        body = {"cartId":cart_id, "bookIsbn":book_isbn, "bookQuantity":quantity}
        request_add_to_cart = Request.create_with_body(body)
        return self.ecommerce_http_api.request_add_to_cart(request_add_to_cart)
    
    def _add_to_cart_and_checkout(self, cart_id, book_isbn, quantity):
        self._add_to_cart(cart_id, book_isbn, quantity)
        return self._checkout_cart(cart_id, "123455", "102025", "Owner Name")
    
    def _list_cart(self, cart_id):
        body = {"cartId":cart_id}
        request_list_cart = Request(body)
        return self.ecommerce_http_api.request_list_cart(request_list_cart)
    
    def _checkout_cart(self, cart_id, credit_card_number, expiration_date, owner_name):
        body = {"cartId":cart_id, "ccn":credit_card_number, "cced":expiration_date, "cco":owner_name}
        request_checkout_cart = Request.create_with_body(body)
        return self.ecommerce_http_api.request_checkout_cart(request_checkout_cart)
    
    def _list_purchases(self, client_id, password):
        body = {"clientId":client_id, "password":password}
        request_list_purchases = Request.create_with_body(body)
        return self.ecommerce_http_api.request_list_purchases(request_list_purchases)
    
    def _add_invalid_credentials_to_login_system(self):
        self.login_system.add_invalid_credentials(INVALID_CREDENTIALS[0], INVALID_CREDENTIALS[1])
    
    def _assert_succes_response(self, response, expected_message):
        expected_body = f"{self.expected_success_body_code()}{self.expected_body_separator()}{expected_message}"
        self._assert_response(response, self.expected_success_status_code(), expected_body)

    def _assert_error_response(self, response, expected_message):
        expected_body = f"{self.expected_error_body_code()}{self.expected_body_separator()}{expected_message}"
        self._assert_response(response, self.expected_error_status_code(), expected_body)

    def _assert_response(self, response, expected_status_code, expected_body):
        self.assertTrue(response.status_code_equals(expected_status_code))
        self.assertTrue(response.body_equals(expected_body))

    def _assert_is_id_success_reponse(self, response):
        self.assertTrue(len(response.body)>2)
        self.assertTrue(response.status_code_equals(self.expected_success_status_code()))
        self.assertEqual(response.body[0], self.expected_success_body_code())
        self.assertEqual(response.body[1], self.expected_body_separator())


if __name__ == '__main__':
    unittest.main()