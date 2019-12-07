# -*- coding: utf-8 -*-

from aquery.query import IQuery


class MysqlQuery(IQuery):
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
    # IGNORE_ERRORS = (mysql.connector.errors.IntegrityError,)


if __name__ == '__main__':
    sql = "select * from student limit 10"
    # MysqlQuery.query_select(sql)

    sql2 = "INSERT INTO student(name, age) VALUES (#{name}, #{age})"
    MysqlQuery.query_insert_many(sql2, [{"name": "Tom", "age": 12}, {"name": "Tom", "age": 12}])

    @MysqlQuery.select("select * from student where id=#{uid}")
    def get_student_by_id(uid):
        return {"uid": uid}


    # print(get_student_by_id(14))
