# -*- coding: utf-8 -*-


class BaseBxException(Exception):
    def __init__(self, error, error_description, *args, **kwargs):
        self.error = error
        self.error_description = error_description
        for k in kwargs:
            v = kwargs[k]
            setattr(self, k, v)
        super(BaseBxException, self).__init__(*args)


class EntityNotFoundException(BaseBxException):
    pass
