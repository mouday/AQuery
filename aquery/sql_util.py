# -*- coding: utf-8 -*-
import re


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
    def raw_replace(sql, data):
        """
        ${key} 进行原样替换
        """
        keys = re.findall(r"\$\{(.*?)\}", sql)

        for key in keys:
            sql = sql.replace(f"${{{key}}}", data[key])

        return sql


if __name__ == '__main__':
    print(SqlUtil.get_field_str(['name', 'age']))
    print(SqlUtil.get_value_str((['name', 'age'])))
    print(SqlUtil.get_field_value_str((['name', 'age'])))
    print(SqlUtil.get_key_list('name', 10))
