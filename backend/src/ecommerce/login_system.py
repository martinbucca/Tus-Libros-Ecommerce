from src.utils.oauth_authentication_system import OAuthAuthenticationSystem

class LoginSystem ():
    def __init__(self) -> None:
        self.authentication_system = OAuthAuthenticationSystem()

    @classmethod
    def invalid_credentials_error_message(cls):
        return "Invalid client id or password"

    def authenticate_client_id_and_password (self, client_id, password):
        try: 
            self.authentication_system.authenticate(client_id, password)
        except:
            raise ValueError(self.invalid_credentials_error_message())