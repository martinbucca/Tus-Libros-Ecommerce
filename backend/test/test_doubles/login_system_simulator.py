class LoginSystemSimulator ():
    def __init__(self) -> None:
        self.invalid_credentials = []

    @classmethod
    def invalid_credentials_error_message(cls):
        return "Invalid client id or password"

    def add_invalid_credentials(self, client_id, password):
        self.invalid_credentials.append((client_id, password))

    def authenticate_client_id_and_password (self, client_id, password):
        if ((client_id, password) in self.invalid_credentials):
            raise ValueError(LoginSystemSimulator.invalid_credentials_error_message())
        

