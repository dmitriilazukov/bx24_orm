# -*- coding: utf-8 -*-


class BaseBusinessLogicException(Exception):
    def __init__(self, error, error_description, *args, **kwargs):
        self.error = error
        self.error_description = error_description
        for k in kwargs:
            v = kwargs[k]
            setattr(self, k, v)
        super(BaseBusinessLogicException, self).__init__(*args)


class EntityNotFoundException(BaseBusinessLogicException):
    pass
