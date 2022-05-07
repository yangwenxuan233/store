import time

import pymysql
from config.DataBaseSettings import DataBaseSettings
from config.ParameterSettings import ParameterSettings


class DataBaseOptions():

    def insert_data(data, table_name):
        # 获取数据库配置
        host = DataBaseSettings.host
        user = DataBaseSettings.user
        password = DataBaseSettings.password
        database = DataBaseSettings.database
        charset = DataBaseSettings.charset
        # 建立数据库连接
        con = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)
        cursor = con.cursor()
        # 获取所有表名
        cursor.execute("show tables")
        tables = cursor.fetchall()
        # 获取所有列名
        title = []
        for i in ParameterSettings.base_parameter:
            if i.startswith("null") is False:
                title.append(i)
        # 如不存在 创建新表
        today = str(time.strftime('%Y-%m-%d', time.localtime()))
        table_name = str(table_name) + '+' + today
        if (table_name.lower(),) not in tables:
            cursor.execute("create table `%s` (`%s` varchar(50))" % (table_name, today))
            con.commit()
            for i in range(0, len(title)):
                cursor.execute("alter table `%s` add column `%s` varchar(50)" % (table_name, title[i]))
        con.commit()
        # 写入数据
        now = str(time.strftime('%H%M%S', time.localtime()))
        cursor.execute("insert into `%s` (`%s`) values ('%s')" % (table_name, today, now))
        con.commit()
        for i in range(0, len(title)):
            cursor.execute("update `%s` set `%s` = '%s' where `%s` = '%s'" % (table_name, title[i], str(data[i]), today, now))
        con.commit()  # 提交
        cursor.close()  # 关闭
        con.close()
        return "<font color='green' size='5'><green>数据库写入成功。</font>"
