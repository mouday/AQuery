# -*- coding: utf-8 -*-
import mysql.connector

from aquery.util.errors import TypeErrorException
from aquery.util.logger import logger


class Database(object):
    """
    配置文档
    https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    """
    # database配置
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

    connect = None
    cursor = None

    def __enter__(self):
        self.open()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def open(cls):
        logger.debug("open database")
        cls.connect = cls.DATABASE_CONNECTOR(**cls.DATABASE_CONFIG)
        cls.cursor = cls.connect.cursor(**cls.CURSOR_CONFIG)

    @classmethod
    def close(cls):
        logger.debug("close database")
        cls.cursor.close()
        cls.connect.close()

    @classmethod
    def execute(cls, sql, data=None, ignore_errors=()):
        """
        :param sql: str
        :param data: dict/list[dict]
        :param ignore_errors: tuple
        :return: cursor
        """
        is_many = False
        # 类型校验
        if isinstance(data, list):
            is_many = True

            for item in data:
                if not isinstance(item, dict):
                    raise TypeErrorException()

        elif isinstance(data, dict):
            pass

        elif data is None:
            pass
        else:
            raise TypeErrorException()

        if cls.connect is None:
            cls.open()

        try:
            if is_many:
                cls.cursor.executemany(sql, data)
            else:
                cls.cursor.execute(sql, data)

        except ignore_errors as e:
            logger.error(e)

        return cls.cursor
