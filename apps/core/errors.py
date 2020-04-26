class CoreException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class CustomerException(CoreException):
    pass

class CorridorException(CoreException):
    pass

class GrilleException(CoreException):
    pass

class CountryException(CoreException):
    pass

class AgentException(CoreException):
    pass

class TransactionNotFoundException(CoreException):
    pass
