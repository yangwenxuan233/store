import pymysql
import json

# 数据库基本操作封装类


class BaseDao():

    def __init__(self, config="mysql.json"):
        # {"host":"localhost", "user":"root", "password":"root", "database":"db_data_spider", "port":3306, "charset": "utf8"}
        self.__config = json.load(open(config))  # dict字典
        self.__connection = None
        self.__cursor = None
        pass

    # 获取数据库连接
    def getConnection(self):
        if self.__connection is not None:
            return self.__connection
        try:
            self.__connection = pymysql.connect(**self.__config)
            # 自动提交事务
            # self.__connection.autocommit(False) # 事务管理的开关
        except Exception as e:
            print("数据库连接失败：" + str(e))
            # print("数据库连接失败：" +  str(e))
            pass
        return self.__connection
        pass

    def execute(self, sql, param=None, ret="tuple"):
        result = 0
        try:
            if ret == "dict":
                self.__cursor = self.getConnection().cursor(cursor=pymysql.cursors.DictCursor)
            else:
                self.__cursor = self.getConnection().cursor()
                pass
            if param:
                result = self.__cursor.execute(sql, param)  # 返回的是条数
            else:
                result = self.__cursor.execute(sql)
        except Exception as e:
            print("数据库执行SQL语句出现异常：" + str(e))
            # print("数据库执行SQL语句出现异常：" + str(e))
            self.__connection.close()
            pass
        return result
        pass

    def commit(self):
        if self.__connection:
            self.__connection.commit()
            pass
        pass

    def rollback(self):
        if self.__connection:
            self.__connection.rollback()
            pass
        pass

    def close(self):
        if self.__connection is not None:
            self.__connection.close()
            pass
        if self.__cursor is not None:
            self.__cursor.close()
            pass
        pass

    def fetchone(self):
        if self.__cursor is not None:
            return self.__cursor.fetchone()
        pass

    def fetchall(self):
        if self.__cursor is not None:
            return self.__cursor.fetchall()
        pass
    pass
