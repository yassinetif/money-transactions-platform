
import logging
CUSTOMER_EXCEPTION_ERROR = 100
CORE_EXCEPTION_ERROR = 200
GRILLE_TARIFAIRE_EXCEPTION_ERROR = 300
COUNTRY_EXCEPTION_ERROR = 400
AGENT_EXCEPTION_ERROR = 500
TRANSACTION_EXCEPTION_ERROR = 600
CORRIDOR_EXCEPTION_ERROR = 700


logger = logging.getLogger(__name__)

class CoreException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
        logger.error(message, errors)
        self.errors = {'response_code': CORE_EXCEPTION_ERROR, 'response_text': self.errors}


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

class EntityException(CoreException):
    pass

class TransactionNotFoundException(CoreException):
    pass

class PartnerApiException(CoreException):
    pass