from src.utils.mercado_pago import MercadoPago

class PaymentProcessor():
    def __init__(self):
        self.processor = MercadoPago()

    @classmethod
    def proccess_payment_error_message(cls):
        return "Unable to process payment"

    def process_payment(self, price_to_charge, credit_card):
        try:
            self.processor.debit(price_to_charge, credit_card)
        except:
            raise ValueError(self.proccess_payment_error_message())