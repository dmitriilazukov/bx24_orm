# -*- coding: utf-8 -*-


from copy import deepcopy


class AbstractField:
    pass


class BxField(AbstractField):
    __slots__ = ('__bx_name', '__prefix', '__value')

    def __init__(self, bx_name, value=None, prefix=""):
        # type: (str, object, str) -> None
        """
        Represents bitrix field
        :param bx_name: name on bitrix portal like UF_CRM_XXXXXX
        :param value: initial value
        :param prefix: prefix before parameters dict, e.g FIELD in ORM module
        """
        self.__value = value
        self.__bx_name = str.upper(bx_name)
        self.__prefix = str.upper(prefix)
        super(BxField, self).__init__()

    @property
    def prefix(self):
        return self.__prefix

    @property
    def bx_name(self):
        return self.__bx_name

    @property
    def value(self):
        # type: () -> object
        """
        Returns copy of contained value to prevent untracked changes
        :return: value
        """
        return deepcopy(self.__value)

    def __set__(self, instance, value):
        self.__value = value

    @staticmethod
    def __format_value(key, value):
        # type: (str, object or list or tuple or set or frozenset) -> dict
        """
        Recursively unwrap field to properly formed dict of params
        :param key: current key
        :param value: value to unwrap
        :return: dict of parameters
        """
        result = {}
        if type(value) in (list, tuple, set, frozenset):
            for i, v in enumerate(value):
                result.update(BxField.__format_value(key + '[{}]'.format(i), v))
        elif type(value) is dict:
            for k in value:
                v = value[k]
                result.update(BxField.__format_value(key + '[{}]'.format(str.upper(k)), v))
        elif value is not None:
            result.update({key: value})
        return result

    @property
    def to_bitrix(self):
        # type: () -> dict
        """
        Converts field into valid parameter or parameters to bitrix
        :return: Dict representing bitrix parameter
        """
        if self.__prefix:
            key = '{}[{}]'.format(self.__prefix, self.__bx_name)
        else:
            key = '{}'.format(self.__bx_name)
        result = self.__format_value(key, self.value)
        return result
