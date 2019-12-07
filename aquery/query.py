# -*- coding: utf-8 -*-

from functools import wraps

import mysql.connector.pooling

from aquery.logger import logger
from aquery.database import Database
from aquery.errors import NotQueryHandlerException
from aquery.sql_util import SqlUtil


class IQuery(object):
    """
    IQuery负责数据查询操作
    不同的操作仅代表不同类型的返回值，也更加语义化

         操作      |    data参数           |       返回值
    ===========================================================
    insert        | dict                  | lastrowid {int}
    insert_many   | list[dict]            | rowcount {int}
    select        | dict                  | fetchall {list[dict]}
    select_one    | dict                  | fetchone {dict}
    update        | dict                  | rowcount {int}
    delete        | dict                  | rowcount {int}

    关键字使用
    #{key} 预编译为 %(key)s
    ${key} 原样替换
    参考 https://www.bbsmax.com/A/n2d9P9gY5D/

    特殊参数
    原样参数: raw_data
    列表参数: list_data
    """

    # database配置
    # 配置文档
    # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    DATABASE_CONFIG = {
        "database": "database",
        "user": "root",
        "password": "123456",
        "host": "127.0.0.1",
        "port": 3306,
        "autocommit": True,
    }

    # cursor配置
    CURSOR_CONFIG = {
        "dictionary": True
    }

    # 驱动连接器
    DATABASE_CONNECTOR = mysql.connector.Connect

    # 特殊参数
    RAW_DATA_KEY = "raw_data"
    LIST_DATA_KEY = "list_data"

    # 数据库操作时，忽略的异常
    IGNORE_ERRORS = ()

    @classmethod
    def _prepare_sql(cls, sql, data=None):

        if isinstance(data, dict):
            raw_data = data.get(cls.RAW_DATA_KEY)

            if raw_data:
                sql = SqlUtil.raw_replace(sql, raw_data)

                data.pop(cls.RAW_DATA_KEY)

        return SqlUtil.compile_sql(sql)

    @classmethod
    def _execute(cls, operator, sql, data=None, **kwargs):
        sql = cls._prepare_sql(sql, data)

        ignore_errors = kwargs.get("IGNORE_ERRORS", ())
        ignore_errors += cls.IGNORE_ERRORS

        logger.debug(sql)
        logger.debug(data)

        with Database(cls.DATABASE_CONFIG, cls.CURSOR_CONFIG, cls.DATABASE_CONNECTOR) as cursor:
            if operator == "insert_many":

                if isinstance(data, list):
                    list_data = data
                elif isinstance(data, dict):
                    list_data = data[cls.LIST_DATA_KEY]
                else:
                    list_data = None

                try:
                    cursor.executemany(sql, list_data)
                except ignore_errors as e:
                    logger.error(e)

                if hasattr(cursor, "statement"):
                    logger.debug(cursor.statement)

                return cursor.rowcount

            else:

                try:
                    cursor.execute(sql, data)
                except ignore_errors as e:
                    logger.error(e)

                if hasattr(cursor, "statement"):
                    logger.debug(cursor.statement)

                if operator == "insert":
                    return cursor.lastrowid

                elif operator == 'select':
                    return cursor.fetchall()

                elif operator == 'select_one':
                    return cursor.fetchone()

                elif operator == 'delete':
                    return cursor.rowcount

    @classmethod
    def query_insert(cls, sql, data=None, **kwargs):
        return cls._execute('insert', sql, data, **kwargs)

    @classmethod
    def query_insert_many(cls, sql, data=None, **kwargs):
        return cls._execute('insert_many', sql, data, **kwargs)

    @classmethod
    def query_update(cls, sql, data=None, **kwargs):
        return cls._execute('update', sql, data, **kwargs)

    @classmethod
    def query_delete(cls, sql, data=None, **kwargs):
        return cls._execute('delete', sql, data, **kwargs)

    @classmethod
    def query_select(cls, sql, data=None, **kwargs):
        return cls._execute('select', sql, data, **kwargs)

    @classmethod
    def query_select_one(cls, sql, data=None, **kwargs):
        return cls._execute('select_one', sql, data, **kwargs)

    @classmethod
    def query(cls, operator, sql, data=None, **kwargs):

        query_func = getattr(cls, f'query_{operator}')

        if not query_func:
            raise NotQueryHandlerException()

        return query_func(sql, data, **kwargs)

    @classmethod
    def _query_wrapper(cls, operator, sql, **outer_kwargs):
        def outer_wrapper(func):
            @wraps(func)
            def inner_wrapper(*args, **inner_kwargs):

                real_data = func(*args, **inner_kwargs)

                if real_data:
                    data = real_data

                elif len(args) > 0:
                    data = args[0]
                else:
                    data = None

                return cls.query(operator, sql, data, **outer_kwargs)

            return inner_wrapper

        return outer_wrapper

    @classmethod
    def select_one(cls, sql, **kwargs):
        return cls._query_wrapper('select_one', sql, **kwargs)

    @classmethod
    def select(cls, sql, **kwargs):
        return cls._query_wrapper('select', sql, **kwargs)

    @classmethod
    def insert(cls, sql, **kwargs):
        return cls._query_wrapper('insert', sql, **kwargs)

    @classmethod
    def insert_many(cls, sql, **kwargs):
        return cls._query_wrapper('insert_many', sql, **kwargs)

    @classmethod
    def update(cls, sql, **kwargs):
        return cls._query_wrapper('update', sql, **kwargs)

    @classmethod
    def delete(cls, sql, **kwargs):
        return cls._query_wrapper('delete', sql, **kwargs)
