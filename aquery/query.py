# -*- coding: utf-8 -*-

from aquery.iquery import IQuery
from aquery.handler.cursor_handler import CursorHandler
from aquery.handler.param_handler import ParamHandler
from aquery.handler.sql_handler import SqlDataHandler


class Query(IQuery):
    # 参数处理器
    PARAM_HANDLER = ParamHandler

    # 执行之前对sql 进行处理
    SQL_HANDLER = SqlDataHandler

    # 执行之前对data 进行处理
    DATA_HANDLER = None

    # 执行之后对 cursor 处理
    CURSOR_HANDLER = None

    # ======================================
    # 普通查询
    # ======================================
    @classmethod
    def query_insert(cls, sql, data=None, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.insert_cursor_handle)

        return cls.query(sql, data, **kwargs)

    @classmethod
    def query_insert_many(cls, sql, data=None, **kwargs):
        kwargs['is_many'] = True
        kwargs.setdefault('cursor_handler', CursorHandler.insert_many_cursor_handle)

        return cls.query(sql, data, **kwargs)

    @classmethod
    def query_update(cls, sql, data=None, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.update_cursor_handle)
        return cls.query(sql, data, **kwargs)

    @classmethod
    def query_delete(cls, sql, data=None, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.delete_cursor_handle)
        return cls.query(sql, data, **kwargs)

    @classmethod
    def query_select(cls, sql, data=None, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.select_cursor_handle)
        return cls.query(sql, data, **kwargs)

    @classmethod
    def query_select_one(cls, sql, data=None, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.select_one_cursor_handle)
        return cls.query(sql, data, **kwargs)

    # ======================================
    # 装饰器方式查询
    # ======================================
    @classmethod
    def select_one(cls, sql, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.select_one_cursor_handle)
        return cls.query_wrapper(sql, **kwargs)

    @classmethod
    def select(cls, sql, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.select_cursor_handle)
        return cls.query_wrapper(sql, **kwargs)

    @classmethod
    def insert(cls, sql, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.insert_cursor_handle)
        return cls.query_wrapper(sql, **kwargs)

    @classmethod
    def insert_many(cls, sql, **kwargs):
        kwargs['is_many'] = True
        kwargs.setdefault('cursor_handler', CursorHandler.insert_many_cursor_handle)
        return cls.query_wrapper(sql, **kwargs)

    @classmethod
    def update(cls, sql, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.update_cursor_handle)
        return cls.query_wrapper(sql, **kwargs)

    @classmethod
    def delete(cls, sql, **kwargs):
        kwargs.setdefault('cursor_handler', CursorHandler.delete_cursor_handle)
        return cls.query_wrapper(sql, **kwargs)
