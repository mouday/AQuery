# -*- coding: utf-8 -*-
import mysql

from aquery.query import Query


class MysqlQuery(Query):
    DATABASE_CONFIG = {
        "database": "data",
        "user": "root",
        "password": "aBc@123456",
        "host": "127.0.0.1",
        "port": 3306,
        "autocommit": True,
        "pool_name": "mypool",  # 使用连接池
        "pool_size": 1,
    }

    # 忽略的异常
    IGNORE_ERRORS = (
        mysql.connector.errors.IntegrityError,
    )

    # mysql-connector-python 连接操作mysql
    # http://www.zhangdongshengtech.com/article-detials/269


# 装饰器方式使用

# 函数参数默认为data, 数据类型是一个dict，或者是None
# 当使用insert_many时 也可以是一个list
@MysqlQuery.select("select * from student where name=#{name}")
def get_student_by_name(name):
    pass


# print(get_student_by_name(name="Tom"))


# 可以自定义函数参数，不过需要返回一个dict 类型的数据，传递给sql 执行器
@MysqlQuery.select("select * from student where id=#{uid}")
def get_student_by_id(uid):
    pass


# print(get_student_by_id(uid=12))

# 可以自定义函数参数，不过需要返回一个dict 类型的数据，传递给sql 执行器
@MysqlQuery.select("select * from student where id in ({uids})")
def get_student_by_ids(uids):
    pass


# print(get_student_by_ids(uids=[13, 23, 33]))

@MysqlQuery.insert("insert into student @{fields} values @{values}")
def insert_student(data):
    pass


# data = {"name": "Tom", 'age': 23}
# print(insert_student(data))

@MysqlQuery.update("update student set @{data} where id = #{uid}")
def update_student(uid, name):
    pass


# print(update_student(uid=12, name=12))


@MysqlQuery.delete("delete from student where id = #{uid}")
def delete_student(uid):
    pass


# print(delete_student(uid=12))

if __name__ == '__main__':
    sql = "select * from student limit 10"
    # print(MysqlQuery.query(sql))

    sql2 = "INSERT INTO student @{fields} VALUES @{values}"
    MysqlQuery.query_insert_many(sql2, [{"name": "Tom", "age": 12}, {"name": "Tom", "age": 12}])
