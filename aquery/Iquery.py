# -*- coding: utf-8 -*-

from functools import wraps

from aquery.database import Database
from aquery.util.logger import logger


class IQuery(Database):
    # 参数处理器
    PARAM_HANDLER = None

    # 执行之前对sql 进行处理
    SQL_HANDLER = None

    # 执行之前对data 进行处理
    DATA_HANDLER = None

    # 执行之后对 cursor 处理
    CURSOR_HANDLER = None

    # 忽略的数据库异常
    IGNORE_ERRORS = ()

    @classmethod
    def query(cls, sql, data=None, **outer_kwargs):
        sql = cls._prepare_sql(sql, data, **outer_kwargs)
        data = cls._prepare_data(data, **outer_kwargs)

        logger.debug("[query] %s %s", sql, data)

        ignore_errors = cls.IGNORE_ERRORS + outer_kwargs.get('ignore_errors', ())
        cursor = cls.execute(sql, data, ignore_errors=ignore_errors)

        return cls._prepare_cursor(cursor, **outer_kwargs)

    @classmethod
    def query_wrapper(cls, sql, **outer_kwargs):
        def outer_wrapper(func):
            @wraps(func)
            def inner_wrapper(*inner_args, **inner_kwargs):
                data = func(*inner_args, **inner_kwargs)

                data = cls._prepare_param(data, outer_kwargs, *inner_args, **inner_kwargs)

                return cls.query(sql, data, **outer_kwargs)

            return inner_wrapper

        return outer_wrapper

    @classmethod
    def _prepare_param(cls, data, outer_kwargs, *inner_args, **inner_kwargs):
        param_handler = outer_kwargs.get("param_handler", cls.PARAM_HANDLER)
        if param_handler:
            data = param_handler.handle(data, outer_kwargs, *inner_args, **inner_kwargs)
        return data

    @classmethod
    def _prepare_sql(cls, sql, data=None, **outer_kwargs):
        sql_handler = outer_kwargs.get("sql_handler", cls.SQL_HANDLER)
        if sql_handler:
            sql = sql_handler.handle(sql, data, **outer_kwargs)
        return sql

    @classmethod
    def _prepare_data(cls, data, **outer_kwargs):
        data_handler = outer_kwargs.get("data_handler", cls.DATA_HANDLER)
        if data_handler:
            data = data_handler.handle(data, **outer_kwargs)
        return data

    @classmethod
    def _prepare_cursor(cls, cursor, **outer_kwargs):
        cursor_handler = outer_kwargs.get("cursor_handler", cls.CURSOR_HANDLER)

        if cursor_handler:
            return cursor_handler(cursor)

        else:
            return cursor
