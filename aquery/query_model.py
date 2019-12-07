# -*- coding: utf-8 -*-
import mysql

from aquery.query import IQuery
from aquery.sql_util import SqlUtil


class IQueryModel(object):
    """
    提供了简单的操作

    使用动态装饰器，以便正常使用继承
    https://www.jianshu.com/p/b2f304823d8f
    """
    query = IQuery

    table = None

    @classmethod
    def get_raw_data(cls, data):

        if isinstance(data, list):
            keys = data[0].keys()
        else:
            keys = data.keys()

        raw_data = {
            "table": cls.table,
            "fields": SqlUtil.get_field_str(keys),
            "values": SqlUtil.get_value_str(keys),
            "data": SqlUtil.get_field_value_str(data)
        }

        return raw_data

    @classmethod
    def insert(cls, data):
        @cls.query.insert("INSERT INTO ${table} ${fields} VALUES ${values}",
                          IGNORE_ERRORS=(mysql.connector.errors.IntegrityError,))
        def inner():
            data.update({"raw_data": cls.get_raw_data(data)})
            return data

        return inner()

    @classmethod
    def insert_many(cls, data):
        @cls.query.insert_many("INSERT INTO ${table} ${fields} VALUES ${values}")
        def inner():
            return {
                "raw_data": cls.get_raw_data(data),
                "list_data": data
            }

        return inner()

    @classmethod
    def select_by_id(cls, uid):
        @cls.query.select_one("select * from ${table} where id = #{uid} limit 1")
        def inner():
            return {"uid": uid, "raw_data": {"table": cls.table}}

        return inner()

    @classmethod
    def delete_by_id(cls, uid):
        @cls.query.delete("delete from ${table} where id = #{uid}")
        def inner():
            return {"uid": uid, "raw_data": {"table": cls.table}}

        return inner()

    @classmethod
    def update_by_id(cls, uid, data):
        @cls.query.delete("update ${table} set ${data} where id = #{uid}")
        def inner():
            extra_data = {
                "uid": uid,
                "raw_data": {
                    "table": cls.table,
                    "data": SqlUtil.get_field_value_str(data)
                }
            }

            data.update(extra_data)
            return data

        return inner()
