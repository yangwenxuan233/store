import pymysql

# 创建connection

connection = pymysql.connect(host='localhost',user='root',password='root',
                             database='db_data_spider',port=3306,charset='utf8')
# pymysql connection 默认是手动commit
# 增加、删除、修改、查询
sql = 'insert into t_job_data(job_name) values("java工程111")'
# 得到cursor 类似java:statement
cursor = connection.cursor()
result = cursor.execute(sql)  # 返回查询到的条数
connection.commit()
print(result)
# 查询   带条件的查询操作
queryStr = 'java'
sql = 'select * from t_job_data where job_name like %s'   # %s占位符
cursor = connection.cursor()
params = ['%' + queryStr + '%']
result = cursor.execute(sql,params)
resultSet = cursor.fetchall()  # 默认返回元组  结果集
print(resultSet)
connection.close()
cursor.close()
