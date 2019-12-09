# -*- coding: utf-8 -*-
import re

from aquery.util.errors import DataEmptyException


class SqlUtil(object):
    @staticmethod
    def get_field_str(keys):
        """
        [name, age] -> (`name`, `age`)
        """
        return "(" + ", ".join([f'`{key}`' for key in keys]) + ")"

    @staticmethod
    def get_value_str(keys):
        """
        [name, age] -> (#{name}, #{age})
        """
        return "(" + ", ".join([f'#{{{key}}}' for key in keys]) + ")"

    @staticmethod
    def get_field_value_str(keys):
        """
        ['name', 'age'] -> `name` = #{name}, `age` = #{age}
        """
        return ", ".join([f"`{key}` = #{{{key}}}" for key in keys])

    @staticmethod
    def get_list_data(key, values):
        keys = SqlUtil.get_key_list(key, len(values))
        return dict(zip(keys, values))

    @classmethod
    def get_data_value_str(cls, data, sql):
        if isinstance(data, list):
            return cls.get_value_str(data[0])
        else:
            return cls.get_value_str(data)

    @classmethod
    def get_data_field_str(cls, data, sql):
        if isinstance(data, list):
            return cls.get_field_str(data[0])
        else:
            return cls.get_field_str(data)

    @classmethod
    def get_auto_data_field_value_str(cls, data, sql):
        variables = cls.get_variable_keys(sql)

        auto_data = {}
        for key, value in data.items():
            if key not in variables:
                auto_data[key] = data[key]

        if not auto_data:
            raise DataEmptyException()

        return cls.get_field_value_str(auto_data)

    @classmethod
    def get_data_field_value_str(cls, data, sql):
        if isinstance(data, list):
            return cls.get_field_value_str(data[0])
        else:
            return cls.get_field_value_str(data)

    @classmethod
    def get_key_list(cls, key, count):
        """
        'name', 5 -> ['name-0', 'name-1', 'name-2', 'name-3', 'name-4']
        """
        return [f"{key}-{index}" for index in range(count)]

    @staticmethod
    def compile_sql(sql):
        """
        sql = "INSERT INTO ${table} #{fields} VALUES #{values}"

        INSERT INTO ${table} %(fields)s VALUES %(values)s

        http://www.mamicode.com/info-detail-2327645.html

        将  #{values} 转换为 %(values)s

        """
        return re.sub(r"#\{(?P<key>.*?)\}", r"%(\g<key>)s", sql)

    @staticmethod
    def raw_data_replace(sql, data):
        """
        ${key} 进行原样替换
        """
        for key, value in data.items():
            sql = sql.replace(f"${{{key}}}", data[key])

        return sql

    @staticmethod
    def auto_data_replace(sql, data):
        """
        @{key} 进行原样替换
        """
        for key, value in data.items():
            sql = sql.replace(f"@{{{key}}}", data[key])

        return sql

    @staticmethod
    def get_variable_keys(sql):
        return re.findall(r"#\{(.*?)\}", sql)

    @staticmethod
    def get_raw_keys(sql):
        return re.findall(r"\$\{(.*?)\}", sql)

    @staticmethod
    def get_auto_keys(sql):
        return re.findall(r"@\{(.*?)\}", sql)

    @classmethod
    def get_list_key(cls, sql):
        return re.findall(r"\(\{(.*?)\}\)", sql)


if __name__ == '__main__':
    print(SqlUtil.get_field_str(['name', 'age']))
    print(SqlUtil.get_value_str((['name', 'age'])))
    print(SqlUtil.get_field_value_str((['name', 'age'])))
    print(SqlUtil.get_key_list('name', 10))
    print(SqlUtil.get_list_key('select * from ${table} where id in ({uid_list}) limit 1'))
