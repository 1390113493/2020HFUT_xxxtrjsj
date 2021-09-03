# -*- coding: utf-8 -*-
# @Time    : 2021/6/16 23:16
# @Author  : HUII
# @FileName: sql.py
# @Software: PyCharm
import pymysql
import configparser


class SqlManage:
    """
    数据库操作
    """

    def __init__(self, table=None):
        """
        初始化数据库
        :param table:
        """
        self.success = False
        self.table = table
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.host = config.get('database', 'host')
        self.port = int(config.get('database', 'port'))
        self.db = config.get('database', 'db_name')
        self.user = config.get('database', 'user')
        self.password = config.get('database', 'password')
        self.connection()

    def __del__(self):
        """
        对象销毁时关闭数据库连接
        :return:
        """
        if self.success:
            self.close()

    def connection(self):
        """
        连接数据库
        :return:
        """
        self.conn = pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user, password=self.password)
        self.cursor = self.conn.cursor()
        self.success = True

    def close(self):
        self.cursor.close()
        self.conn.close()

    def check_connect(func):
        def check(self, *args, **kwargs):
            try:
                self.conn.ping()
            except:
                self.connection()
            return func(self, *args, **kwargs)

        return check

    @check_connect
    def select(self, params=None, selects=None):
        """
        查找
        :param params:
        :return:
        """
        if selects:
            select_str = ', '.join(selects)
        else:
            select_str = '*'
        if params and ''.join(params.values()):
            for k, v in params.items():
                if isinstance(params[k], str) and params[k] != '':
                    params[k] = f"'{v}'"
            sql = f"select {select_str} from {self.table} where {' and '.join([f'{k}={v}' for k, v in params.items() if v])};"
        else:
            sql = f"select {select_str} from {self.table};"
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    @check_connect
    def insert(self, params):
        """
        新增数据
        :param params:
        :return:
        """
        for k, v in params.items():
            if v:
                params[k] = f"'{v}'"
            else:
                params[k] = 'null'
        # print(params)
        sql = f'insert into {self.table}({(",".join(params.keys()))}) values({", ".join(params.values())});'
        print(sql)
        return self.cursor.execute(sql)

    @check_connect
    def delete(self, params):
        """
        删除数据
        :param params:
        :return:
        """
        for k, v in params.items():
            if v:
                params[k] = f"'{v}'"
            else:
                params[k] = 'null'
        sql = f'delete from {self.table} where {" and ".join([f"{k}={v}" for k, v in params.items()])};'
        # print(sql)
        return self.cursor.execute(sql)

    @check_connect
    def update(self, params1, params2):
        """
        修改数据
        :param params1:
        :param params2:
        :return:
        """
        for k, v in params1.items():
            if v:
                params1[k] = f"'{v}'"
            else:
                params1[k] = 'null'
        for k, v in params2.items():
            if v:
                params2[k] = f"'{v}'"
            else:
                params2[k] = 'null'
        sql = f'update {self.table} set {", ".join([f"{k}={v}" for k, v in params2.items()])} where {" and ".join([f"{k}={v}" for k, v in params1.items()])};'
        # print(sql)
        return self.cursor.execute(sql)

    @check_connect
    def carry(self, sql):
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


def test_connect():
    """
    测试数据库连接是否正常
    """
    try:
        SqlManage()
        return True
    except pymysql.err.OperationalError:
        return False