# -*- coding: utf-8 -*-


class NotQueryHandlerException(Exception):
    pass


class RawDataNotFindException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AutoDataNotFindException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class TypeErrorException(Exception):
    pass


class DataEmptyException(Exception):
    pass
