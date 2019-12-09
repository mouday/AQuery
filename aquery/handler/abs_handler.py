# -*- coding: utf-8 -*-


from abc import abstractmethod, ABC


class ParamHandlerAbstract(ABC):
    """
    must return data
    outer_kwargs is ref data
    """

    @abstractmethod
    def handle(cls, data, outer_kwargs, *args, **kwargs):
        pass


class SqlHandlerAbstract(ABC):
    """
    must return sql
    """

    @abstractmethod
    def handle(cls, sql, data, **kwargs):
        pass


class DataHandlerAbstract(ABC):
    """
    must return data
    """

    @abstractmethod
    def handle(cls, data, operator, **kwargs):
        pass


class CursorHandlerAbstract(ABC):
    """
    must return data or cursor
    """

    @abstractmethod
    def handle(cls, cursor, **outer_kwargs):
        pass
