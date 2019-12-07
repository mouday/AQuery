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