# -*- coding: utf-8 -*-
from aquery.handler.abs_handler import SqlHandlerAbstract
from aquery.util.errors import RawDataNotFindException, TypeErrorException, AutoDataNotFindException
from aquery.util.logger import logger
from aquery.util.sql_util import SqlUtil


class SqlDataHandler(SqlHandlerAbstract):
    # 默认的变量获取器
    AUTO_DATA_GETTER = {
        "fields": SqlUtil.get_data_field_str,
        "values": SqlUtil.get_data_value_str,
        "data": SqlUtil.get_auto_data_field_value_str
    }

    @classmethod
    def handle(cls, sql, data, **kwargs):
        sql = cls.raw_data_handle(sql, data, **kwargs)
        sql = cls.list_data_handler(sql, data, **kwargs)
        sql = cls.auto_data_handler(sql, data, **kwargs)
        sql = cls.sql_compile_handler(sql, data, **kwargs)
        return sql

    @classmethod
    def raw_data_handle(cls, sql, data, **kwargs):
        """
        原样数据
        ${key}
        优先级 data > class_object
        """

        raw_keys = SqlUtil.get_raw_keys(sql)

        # 如果有需要替换的原样数据
        if not raw_keys:
            return sql

        logger.debug("[raw_keys] %s", raw_keys)

        raw_data = {}

        # 从class_object 中获取数据
        class_object = kwargs.get("class_object", None)
        if class_object:
            for key in raw_keys:
                if hasattr(class_object, key):
                    raw_data[key] = getattr(class_object, key)

        # 从data中获取数据
        if isinstance(data, dict):
            for key in raw_keys:
                if key in data:
                    raw_data[key] = data.pop(key)

        # 数据检查
        for key in raw_keys:
            if key not in raw_data.keys():
                raise RawDataNotFindException(key)

        # 原样替换
        return SqlUtil.raw_data_replace(sql, raw_data)

    @classmethod
    def auto_data_handler(cls, sql, data, **kwargs):
        """
        @{key}
        :return:
        """
        auto_keys = SqlUtil.get_auto_keys(sql)

        # 如果有需要替换的原样数据
        if not auto_keys:
            return sql

        logger.debug("[auto_keys] %s", auto_keys)

        auto_data = {}
        for key in auto_keys:
            value = cls.AUTO_DATA_GETTER.get(key)

            if callable(value):
                value = value(data, sql)

            if value:
                auto_data[key] = value
            else:
                raise AutoDataNotFindException(key)

        return SqlUtil.auto_data_replace(sql, auto_data)

    @classmethod
    def list_data_handler(cls, sql, data, **kwargs):
        """
        ({list}) -> (#{list-1}, #{list-2}...)
        """
        list_keys = SqlUtil.get_list_key(sql)

        if not list_keys:
            return sql

        logger.debug("[list_keys] %s", list_keys)

        for key in list_keys:
            value = data.pop(key)
            if isinstance(value, list):
                in_data = SqlUtil.get_list_data(key, value)

                # 确认没有交集才进行添加，否则会污染数据
                if not data.keys().isdisjoint(in_data.keys()):
                    raise Exception("有重复数据，不能进行添加")

                data.update(in_data)
                value = SqlUtil.get_value_str(in_data.keys())

                sql = sql.replace(f"({{{key}}})", value)
            else:
                raise TypeErrorException()

        return sql

    @classmethod
    def sql_compile_handler(cls, sql, data, **kwargs):
        """
        #{key}
        """
        return SqlUtil.compile_sql(sql)
