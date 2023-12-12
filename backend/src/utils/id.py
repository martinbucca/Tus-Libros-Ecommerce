from uuid import uuid4, UUID

class Id():
    def __init__(self):
        pass
    
    @classmethod
    def generate(cls):
        return uuid4()
    
    @classmethod
    def create_from_string(cls, id):
        return UUID(id)
    
    @classmethod
    def create_as_string(cls):
        return str(cls.generate())