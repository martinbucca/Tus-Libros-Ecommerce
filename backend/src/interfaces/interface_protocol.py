import flask

class Request ():
    def __init__ (self, body={}) -> None:
        self.body = body
    
    @classmethod
    def create_with_body(cls, body):
        return Request(body)

    @classmethod
    def create_from_http_request(cls, http_request):
        return Request(http_request.args.to_dict())
    
class Response():
    def __init__ (self, body, status_code) -> None:
        self.body = body
        self.status_code = status_code

    @classmethod
    def success_body_code(cls):
        return "0"
    @classmethod
    def error_body_code(cls):
        return "1"
    @classmethod
    def response_body_separator(self):
        return "|"
    @classmethod
    def success_status_code(self):
        return 200
    @classmethod
    def error_status_code(self):
        return 200
    
    @classmethod
    def generate_success_response_with(cls, message):
        body = f"{cls.success_body_code()}{cls.response_body_separator()}{message}"
        success_status_code = cls.success_status_code()
        return Response(body, success_status_code)
    
    @classmethod
    def generate_error_response_with(cls, message):
        body = f"{cls.error_body_code()}{cls.response_body_separator()}{message}"
        error_status_code = cls.error_status_code()
        return Response(body, error_status_code)
    
    def status_code_equals(self, status_code):
        return status_code == self.status_code
    
    def body_equals(self, body):
        return body == self.body
    
    def to_http_response(self):
        return flask.Response(self.body, status=self.status_code)