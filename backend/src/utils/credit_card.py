class CreditCard():
    def __init__(self, credit_card_number, expiration_month_of_year, owner_name) -> None:
        self._validate_owner_name(owner_name)
        self._validate_credit_card_number(credit_card_number)
        self.credit_card_number = credit_card_number
        self.expiration_month_of_year = expiration_month_of_year
        self.owner_name = owner_name

    @classmethod
    def with_credit_card_number_expiration_month_of_year_and_owner(cls, credit_card_number, expiration_date, owner_name):
        return CreditCard(credit_card_number, expiration_date, owner_name)
        
    @classmethod
    def invalid_card_data_error_message(cls):
        return "Invalid card data"

    def number(self):
        return self.credit_card_number
    
    def is_expired(self, month_of_year):
        return self.expiration_month_of_year.is_before(month_of_year)

    def _validate_owner_name(self, owner_name):
        self._validate_credit_card_owner_name_length(owner_name)
        self._validate_credit_card_owner_name_characters(owner_name)

    def _validate_credit_card_owner_name_length(self, owner_name):
        if (len(owner_name) == 0 or len(owner_name)>30):
            raise ValueError(self.invalid_card_data_error_message())
    
    def _validate_credit_card_owner_name_characters(self, owner_name):
        for character in owner_name:
            if (not character.isalpha() and character != " "):
                raise ValueError(self.invalid_card_data_error_message())
        
    def _validate_credit_card_number(self, credit_card_number):
        self._validate_credit_card_number_length(credit_card_number)
        self._validate_credit_card_number_digits(credit_card_number)
        
    def _validate_credit_card_number_length(self, credit_card_number):
        if (len(credit_card_number) < 1 or len(credit_card_number) > 16):
            raise ValueError(self.invalid_card_data_error_message())
    
    def _validate_credit_card_number_digits(self, credit_card_number):
        if (not credit_card_number.isdigit()):
            raise ValueError(self.invalid_card_data_error_message())