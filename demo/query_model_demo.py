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
