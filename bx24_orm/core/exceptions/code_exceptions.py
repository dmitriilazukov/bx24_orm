NOT_JSON_RESPONSE = 'NOT_JSON_RESPONSE'
UNEXPECTED_HTTP_CODE = 'UNEXPECTED_HTTP_CODE'
QUERY_LIMIT_EXCEEDED = 'QUERY_LIMIT_EXCEEDED'
NO_AUTH_FOUND = 'NO_AUTH_FOUND'
ERROR_METHOD_NOT_FOUND = 'ERROR_METHOD_NOT_FOUND'
NETWORK_ERROR = 'NETWORK_ERROR'


class BxException(Exception):
    def __init__(self, error, error_description):
        super(Exception, self).__init__()
        self.error = error
        self.error_description = error_description

    def __str__(self):
        return str((self.error, self.error_description))


class NotFoundException(BxException):
    pass


class InvalidQueryException(BxException):
    pass


class InvalidTokenException(BxException):
    pass


class InvalidRequestException(BxException):
    pass


class RequestFailedException(BxException):
    pass


class QueryLimitExceededException(RequestFailedException):
    pass


class NotJsonResponseException(RequestFailedException):
    pass


class TokenExpiredException(InvalidTokenException):
    pass


class TokenNotFoundException(InvalidTokenException):
    pass


class UnexpectedResponseCodeException(RequestFailedException):
    pass
