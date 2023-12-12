from flask import Flask, request, Response
from src.interfaces.ecommerce_http_api import EcommerceHttpAPI
from src.interfaces.ecommerce_system import EcommerceSystem
from src.interfaces.interface_protocol import Request
from src.ecommerce.login_system import LoginSystem
from src.utils.current_date_and_time import CurrentDateAndTimeProvider
from src.ecommerce.payment_processor import PaymentProcessor
from src.utils.constants import CATALOUGE

class Server:
    def __init__(self):
        self.interface = self._generate_interface()
        self.app = Flask(__name__)
        self.add_routes()

    @classmethod
    def run_with_host_and_port(cls, host, port):
        server = Server()
        server.run(host, port)
    
    @classmethod
    def create_cart_route(cls):
        return "/createCart"
    @classmethod
    def add_to_cart_route(self):
        return "/addToCart"
    @classmethod
    def list_cart_route(self):
        return "/listCart"
    @classmethod
    def checkout_cart_route(self):
        return "/checkOutCart"
    @classmethod
    def list_purchases_route(self):
        return "/listPurchases"

    
    def run(self, host, port):
        self.app.run(debug=True, host=host, port=port)

    def define_route(self, path, methods=['GET']):
        def add_block(block_to_run):
            self.app.add_url_rule(path, block_to_run.__name__, view_func=block_to_run, methods=methods)
            return block_to_run
        return add_block
    
    def add_routes(self):
        self.define_route(path=self.create_cart_route(), methods=['GET'])(self.create_cart)
        self.define_route(path=self.add_to_cart_route(), methods=['GET'])(self.add_to_cart)
        self.define_route(path=self.list_cart_route(), methods=['GET'])(self.list_cart)
        self.define_route(path=self.checkout_cart_route(), methods=['GET'])(self.checkout_cart)
        self.define_route(path=self.list_purchases_route(), methods=['GET'])(self.list_purchases)

    def create_cart(self):
        interface_request = Request.create_from_http_request(request)
        interface_response = self.interface.request_create_cart(interface_request)
        return interface_response.to_http_response()
    
    def add_to_cart(self):
        interface_request = Request.create_from_http_request(request)
        interface_response = self.interface.request_add_to_cart(interface_request)
        return interface_response.to_http_response()

    def list_cart(self):
        interface_request = Request.create_from_http_request(request)
        interface_response = self.interface.request_list_cart(interface_request)
        return interface_response.to_http_response()
    
    def checkout_cart(self):
        interface_request = Request.create_from_http_request(request)
        interface_response = self.interface.request_checkout_cart(interface_request)
        return interface_response.to_http_response()
    
    def list_purchases(self):
        interface_request = Request.create_from_http_request(request)
        interface_response = self.interface.request_list_purchases(interface_request)
        return interface_response.to_http_response()
    
    def _generate_interface(self):
        current_date_and_time = CurrentDateAndTimeProvider()
        login_system = LoginSystem()
        payment_processor = PaymentProcessor()
        ecommerce_system = EcommerceSystem.with_login_system_catalogue_datetime_provider_and_payment_processor(login_system, CATALOUGE, current_date_and_time, payment_processor)
        return EcommerceHttpAPI.with_ecommerce_system(ecommerce_system)