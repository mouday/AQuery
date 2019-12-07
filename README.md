
AQuery 一个注解方式操作数据库的便捷库 


IQuery类负责数据查询操作
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
    
 ## Demo
 ```python
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
        "pool_name": "mypool",
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
``` 
 
 ```python
# -*- coding: utf-8 -*-

from demo.query_demo import MysqlQuery
from aquery.query_model import IQueryModel


class BaseQueryModel(IQueryModel):
    query = MysqlQuery


class StudentModel(BaseQueryModel):
    table = "student"


if __name__ == '__main__':
    print(StudentModel.insert({"name": "Tom", "age": 12,'id': 12}))

    # print(StudentModel.insert_many([{"name": "Tom", "age": 12}]))

    # print(StudentModel.update_by_id(27, {"name": "--T'om", "age": 13}))
```