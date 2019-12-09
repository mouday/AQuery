# -*- coding: utf-8 -*-
from aquery.handler.abs_handler import CursorHandlerAbstract
from aquery.util.logger import logger


class CursorHandler(CursorHandlerAbstract):
    @classmethod
    def insert_cursor_handle(cls, cursor, **outer_kwargs):
        cls.handle(cursor, **outer_kwargs)
        return cursor.lastrowid

    @classmethod
    def insert_many_cursor_handle(cls, cursor, **outer_kwargs):
        cls.handle(cursor, **outer_kwargs)
        return cursor.rowcount

    @classmethod
    def update_cursor_handle(cls, cursor, **outer_kwargs):
        cls.handle(cursor, **outer_kwargs)
        return cursor.rowcount

    @classmethod
    def delete_cursor_handle(cls, cursor, **outer_kwargs):
        cls.handle(cursor, **outer_kwargs)
        return cursor.rowcount

    @classmethod
    def select_cursor_handle(cls, cursor, **outer_kwargs):
        cls.handle(cursor, **outer_kwargs)
        return cursor.fetchall()

    @classmethod
    def select_one_cursor_handle(cls, cursor, **outer_kwargs):
        cls.handle(cursor, **outer_kwargs)
        return cursor.fetchone()

    @classmethod
    def handle(cls, cursor, **outer_kwargs):
        if hasattr(cursor, "statement"):
            logger.debug('[statement] %s', cursor.statement)
