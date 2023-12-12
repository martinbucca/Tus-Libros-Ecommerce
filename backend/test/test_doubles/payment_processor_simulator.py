class PaymentProcessorSimulator():
    def __init__(self):
        self.accept_payment = True
        self.has_previously_processed_payment = False

    @classmethod
    def with_behaviour_to_fail(cls):
        payment_processor = PaymentProcessorSimulator()
        payment_processor.set_behaviour_to_fail()
        return payment_processor

    @classmethod
    def with_behaviour_to_succeed(cls):
        payment_processor = PaymentProcessorSimulator()
        return payment_processor

    @classmethod
    def proccess_payment_error_message(cls):
        return "Unable to process payment"

    def set_behaviour_to_fail(self):
        self.accept_payment = False
    
    def process_payment(self, total_price, credit_card):
        if (not self.accept_payment):
            raise ValueError(self.proccess_payment_error_message())
        self.has_previously_processed_payment = True

    def has_processed_payment(self):
        return self.has_previously_processed_payment
        
    