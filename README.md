
AQuery 一个注解方式操作数据库的便捷库 

安装
```bash
pip install AQuery
```

1、IQuery负责数据查询操作

    不同的操作仅代表不同类型的返回值，参数都是一样 也更加语义化

         操作          | 装饰器方式   | data参数    |       返回值
    ===========================================================
    query_insert      | insert      | dict       | lastrowid {int}
    query_insert_many | insert_many | list[dict] | rowcount {int}
    query_select      | select      | dict       | fetchall {list[dict]}
    query_select_one  | select_one  | dict       | fetchone {dict}
    query_update      | update      | dict       | rowcount {int}
    query_delete      | delete      | dict       | rowcount {int}

    2、关键字使用
    #{key}  变量参数 预编译为 %(key)s
    ${key}  原样替换 ${key} -> value, 如果携带的data中不存在，会尝试从 class_object 参数中获取
    @{key}  自动参数 已实现特殊参数：fields，values, data
    ({key}) 列表参数  ({key}) -> (1, 2, 3)
    
    参考 https://www.bbsmax.com/A/n2d9P9gY5D/

    4、kwargs 参数
        class_object  传递一个类对象，用于从类中获取原样数据
        ignore_errors 执行SQL 时忽略的异常

    5、函数方式查询
    当使用query_* 查询是，第一个参数sql，第二个参数data是dict类型

    6、装饰器方式查询
    当使用装饰器方式时，sql通过装饰器传递，而data通过被装饰的函数返回值传递，
    如果函数没有返回值，则取被装饰函数的第一个参数，或取全部关键字参数

    应用场景：
        1、如果函数传入一个dict 或list，不需要携带额外参数，可以简写

        @query.select("insert into student(name, age) values (#{name}, #{age})")
        def insert(data):
            pass

        insert({'name': "Tom", 'age': 23})

        2、如果需要有原样替换的字符串，需要data 返回
        @query.select("insert into student ${field} values ${value}")
        def insert(data):
            data.update({
                'field': '(name, age)',
                'value': '(#{name}, #{age})'
            })
            return data

        insert({'name': "Tom", 'age': 23})

 ## Demo
 ```python
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

``` 
 
 ```python
# -*- coding: utf-8 -*-

from demo.query_demo import MysqlQuery
from aquery.query_model import IQueryModel


class BaseQueryModel(IQueryModel):
    query = MysqlQuery


class StudentModel(BaseQueryModel):
    table = "student"

    select_fields = "name, age"

    @classmethod
    @MysqlQuery.select('select ${select_fields} from ${table} where name = #{name}')
    def select_by_name(cls, name):
        pass


if __name__ == '__main__':
    pass

    # print(StudentModel.insert_many([{"name": "Tom", "age": 12}]))

    # print(StudentModel.insert({"name": "Tom", "age": 12}))

    # print(StudentModel.select_by_id(27))

    # print(StudentModel.delete_by_id(27))

    # print(StudentModel.select_by_ids([27, 25]))

    # print(StudentModel.update_by_id(27, {'id': 26, "name": "--T'om", "age": 13}))

    print(StudentModel.select_by_name(name='Jack'))

```