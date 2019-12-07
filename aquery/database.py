# -*- coding: utf-8 -*-
from aquery.logger import logger


class Database(object):
    database_config = None
    cursor_config = None
    connector = None

    connect = None
    cursor = None

    def __init__(self, database_config, cursor_config, connector):
        self.database_config = database_config
        self.cursor_config = cursor_config
        self.connector = connector

    def __enter__(self):
        self.open()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        logger.debug("open database")
        self.connect = self.connector(**self.database_config)
        self.cursor = self.connect.cursor(**self.cursor_config)

    def close(self):
        logger.debug("close database")
        self.cursor.close()
        self.connect.close()
