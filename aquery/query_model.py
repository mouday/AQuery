# -*- coding: utf-8 -*-

from aquery.query import Query


class IQueryModel(object):
    """
    提供了简单的操作

    使用动态装饰器，以便正常使用继承
    https://www.jianshu.com/p/b2f304823d8f
    """
    query = Query

    table = None

    @classmethod
    def insert(cls, data):
        sql = "INSERT INTO ${table} @{fields} VALUES @{values}"
        return cls.query.query_insert(sql, data, class_object=cls)

    @classmethod
    def insert_many(cls, data):
        sql = "INSERT INTO ${table} @{fields} VALUES @{values}"
        return cls.query.query_insert_many(sql, data, class_object=cls)

    @classmethod
    def select_by_id(cls, uid):
        data = {"uid": uid}
        sql = "select * from ${table} where id = #{uid} limit 1"
        return cls.query.query_select_one(sql, data, class_object=cls)

    @classmethod
    def select_by_ids(cls, uid_list):
        data = {"uid_list": uid_list}

        sql = "select * from ${table} where id in ({uid_list}) limit 1"

        return cls.query.query_select_one(sql, data, class_object=cls)

    @classmethod
    def delete_by_id(cls, uid):
        sql = "delete from ${table} where id = #{uid}"
        return cls.query.query_delete(sql, {"uid": uid}, class_object=cls)

    @classmethod
    def update_by_id(cls, uid, data):
        sql = "update ${table} set @{data} where id = #{uid}"
        data['uid'] = uid
        return cls.query.query_update(sql, data, class_object=cls)
