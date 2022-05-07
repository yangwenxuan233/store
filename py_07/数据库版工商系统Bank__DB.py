import random
from DBUtils import update
from DBUtils import select
import pymysql

# 全局增删改的方法
def update(sql,param):
	con = pymysql.connect(host="localhost",user="root",password="root",database="bank")
	cursor = con.cursor()
	cursor.execute(sql,param)
	con.commit()
	cursor.close()
	con.close()


# 全局做查询的方法
def select(sql,param):
	con = pymysql.connect(host="localhost",user="root",password="root",database="bank")
	cursor = con.cursor()
	cursor.execute(sql,param)
	con.commit()
	data = cursor.fetchall()
	cursor.close()
	con.close()
	return data

	

# 导包、全局变量

# 1. 空的银行的库 ： 100个
users = {}  # 该数据库将不在需要，使用真实的mysql数据进行存储数据

# 2.银行的名称写死
bank_name = "中国工商银行的昌平支行"

# 打印欢迎页面
def welcome():
    print("---------------------------------")
    print("-  中国工商银行账户管理系统V1.0   -")
    print("---------------------------------")
    print("-   1.开户                       -")
    print("-   2.存钱                       -")
    print("-   3.取钱                       -")
    print("-   4.转账                       -")
    print("-   5.查询                       -")
    print("-   6.Bye!                       -")
    print("----------------------------------")

# 银行的开户逻辑
def bank_addUser(account,username,password,country,province,street,door):
    # 判断是否已满
    sql = "select count(*) from user"
    data = select(sql,[]) # ((72),(),())
    if data[0][0] >= 100:
        return 3
    # 判断是否存在
    sql1 = "select * from user where account = %s"
    data1 = select(sql1,account) #(("张三"),(“李四”))
    if len(data1) != 0:
        return 2
    #正常开户
    # 数据存到数据库里
    sql2 = "insert into user values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    param2 = [account,username,password,country,province,street,door,0,"2021-08-09",bank_name]
    update(sql2,param2)
    return 1


# 用户开户方法
def addUser():
    # 随机获取账号
    li = ["1","2","3","4","5","6","7","8","9","0","a","b","c","e","f"]
    account = ""
    for i in range(8):
        index = random.randint(0, len(li) - 1)
        account = account + li[index]
    name = input("请输入用户名：")
    password = input("请输入您的密码（6位数字）：")
    print("接下来要输入您的地址信息：")
    country = input("\t输入国家：")
    province = input("\t输入省份：")
    street =  input("\t输入街道：")
    door = input("\t输入门牌号：")
    # 余额不允许第一次输入，需要存钱

    status = bank_addUser(account,name,password,country,province,street,door)
    if status == 1:
        print("恭喜开户成功！")
        info = '''
            ------------个人信息----------------
            账号：%s,
            用户名：%s,
            取款密码：%s,
            地址信息：
                国家：%s,
                省份：%s,
                街道：%s,
                门牌号：%s,
            余额：%s,
            开户行：%s
            -----------------------------------
        '''
        print(info % (account,name,password,country,province,street,door,0,bank_name))

    elif status == 2:
        print("对不起，该用户已存在！请稍后重试！！！")
    elif status == 3:
        print("对不起，该银行库已满，请携带证件到其他银行办理！！！")



while True:
    welcome()
    num = input("请输入您的业务编号：")
    if num.isdigit():
        num = int(num)
        if num == 1:
            addUser()
        elif num == 2:
            pass
        elif num == 3:
            pass
        elif num == 4:
            pass
        elif num == 5:
            pass
        elif num == 6:
            print("拜拜了您嘞，欢迎下次光临！！！")
            break
        else:
            print("输入非法！请重新输入！！！别瞎弄！！！")
    else:
        print("您输入非法！请重新输入！！！")







































