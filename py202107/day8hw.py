import random
import pymysql


class Bank():

    # 全局增删改
    def update(sql, param):
        con = pymysql.connect(host="localhost", user="root", password="root", database="bank")
        cursor = con.cursor()
        cursor.execute(sql, param)
        con.commit()
        cursor.close()
        con.close()

    # 全局查询
    def select(sql, param):
        con = pymysql.connect(host="localhost", user="root", password="root", database="bank")
        cursor = con.cursor()
        cursor.execute(sql, param)
        con.commit()
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return data

    # 新增db_bank_data表数据
    def bank_data_in(username, password, IDcard, account, country, province, street, gate, money, bank_name):
        sql = "insert into db_bank_data values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        param = [username, password, IDcard, account, country, province, street, gate, money, bank_name]
        Bank.update(sql, param)

    # 查询信息
    def data_search(account):
        sql = "select * from db_bank_data where account = %s"
        param = [account]
        return Bank.select(sql, param)[0]

    # 资金流入
    def money_in(account, money):
        sql = "update db_bank_data set money = money + %s where account = %s"
        param = [money, account]
        Bank.update(sql, param)

    # 资金流出
    def money_out(account, money):
        sql = "update db_bank_data set money = money - %s where account = %s"
        param = [money, account]
        Bank.update(sql, param)

    # 获取余额
    def money_search(account):
        sql = "select money from db_bank_data where account = %s"
        param = [account]
        return Bank.select(sql, param)[0][0]

    # 获取密码
    def password_search(account):
        sql = "select password from db_bank_data where account = %s"
        param = [account]
        return Bank.select(sql, param)[0][0]

    # 判断账号是否在数据库内，是返回True，否返回False
    def bank_judge(account):
        sql = "select * from db_bank_data"
        param = []
        data = Bank.select(sql, param)
        for i in data:
            if account in i:
                return True
        return False

    # 入口程序
    def welcome():
        print("*************************************")
        print("*      中国工商银行昌平支行           *")
        print("*************************************")
        print("*  1.开户                            *")
        print("*  2.存钱                            *")
        print("*  3.取钱                            *")
        print("*  4.转账                            *")
        print("*  5.查询                            *")
        print("*  6.退出                            *")
        print("**************************************")

    # 银行的开户逻辑
    def bank_addUser(username, password, IDcard, account, country, province, street, gate, money, bank_name):
        # 1.判断数据库是否已满
        sql = "select count(*) from db_bank_data"
        data = Bank.select(sql, [])[0]
        if data[0] >= 100:
            return 3
        # 2.判断用户是否存在
        sql = "select count(*) from db_bank_data, db_user_data where db_bank_data.idcard = db_user_data.idcard"
        data = Bank.select(sql, [])[0]
        if data[0] > 1:
            return 2
        # 3.正常开户
        Bank.bank_data_in(username, password, IDcard, account, country, province, street, gate, money, bank_name)
        sql = "insert into db_user_data values(%s, %s, %s)"
        param = [username, IDcard, account]
        Bank.update(sql, param)
        return 1

    # 用户的开户的操作逻辑
    def addUser():
        username = input("请输入您的用户名：")
        password = int(input("请输入您的开户密码："))
        IDcard = input("请输入您的身份证号：")
        account = random.randint(10000000, 99999999)  # 随机产生8为数字
        country = input("请输入您的国籍：")
        province = input("请输入您的居住省份：")
        street = input("请输入您的街道：")
        gate = input("请输入您的门牌号：")
        money = int(input("请输入您的开户初始余额："))
        bank_name = "中国工商银行昌平回龙观支行"  # 银行名称写死的
        status = Bank.bank_addUser(username, password, IDcard, account, country, province, street, gate, money, bank_name)
        if status == 3:
            print("对不起，用户库已满，请携带证件到其他银行办理！")
        elif status == 2:
            print("对不起，该用户已存在！请勿重复开户！")
        elif status == 1:
            print("开户成功！以下是您的个人开户信息：")
            info = '''
            ----------个人信息------
            用户名：%s
            身份证号：%s
            账号：%s
            密码：%s
            地址信息
            国家：%s
            省份：%s
            街道：%s
            门牌号: %s
            余额：%s
            开户行地址：%s
            ------------------------
        '''
            print(info % (username, IDcard, account, password, country, province, street, gate, money, bank_name))

    # 存钱逻辑
    def bank_savemoney(account_save, money_save):
        sql = "select * from db_bank_data"
        data = Bank.select(sql, [])
        for i in data:
            if account_save in i:
                Bank.money_in(account_save, money_save)
                return True
        return False

    # 存钱操作逻辑
    def savemoney():
        account_save = int(input("请输入您的账号:"))
        money_save = int(input("请输入您的存款金额:"))
        status = Bank.bank_savemoney(account_save, money_save)
        if status is True:
            print("存钱成功！当前余额：", Bank.money_search(account_save))
            pass
        else:
            print("该用户不存在！")
            pass

    # 取钱逻辑
    def bank_getmoney(account_get, password_get, money_get):
        if Bank.bank_judge(account_get) is False:
            return 1
        elif password_get != Bank.password_search(account_get):
            return 2
        elif money_get > Bank.money_search(account_get):
            return 3
        else:
            Bank.money_out(account_get, money_get)
            return 0

    # 取钱操作逻辑
    def getmoney():
        account_get = int(input("请输入您的账号："))
        password_get = int(input("请输入您的密码："))
        money_get = int(input("请输入您的取款金额："))
        status = Bank.bank_getmoney(account_get, password_get, money_get)
        if status == 1:
            print("该用户不存在！")
            pass
        elif status == 2:
            print("密码错误！")
            pass
        elif status == 3:
            print("余额不足！")
            pass
        else:
            print("取款成功！当前余额：", Bank.money_search(account_get))
            pass

    # 转账逻辑
    def bank_trans(account_out, account_in, password_out, money_trans):
        if any([Bank.bank_judge(account_out), Bank.bank_judge(account_in)]) is False:
            return 1
        elif password_out != Bank.password_search(account_out):
            return 2
        elif money_trans > Bank.money_search(account_out):
            return 3
        else:
            Bank.money_out(account_out, money_trans)
            Bank.money_in(account_in, money_trans)
            return 0

    # 转账操作逻辑
    def trans():
        account_out = int(input("请输入您要转出的账号："))
        account_in = int(input("请输入您要转入的账号："))
        password_out = int(input("请输入您要转出的密码："))
        money_trans = int(input("请输入您要转出的金额："))
        status = Bank.bank_trans(account_out, account_in, password_out, money_trans)
        if status == 1:
            print("用户不存在！")
            pass
        elif status == 2:
            print("密码错误！")
            pass
        elif status == 3:
            print("余额不足！")
            pass
        else:
            print("转账成功！")
            print("转出账户余额：", Bank.money_search(account_out))
            print("转入账户余额：", Bank.money_search(account_in))
            pass

    # 查询账户逻辑
    def search():
        account_sch = int(input("请输入您要查询的账号："))
        password_sch = int(input("请输入您要查询的密码："))
        if Bank.bank_judge(account_sch) is True:
            if password_sch != Bank.password_search(account_sch):
                print("密码错误！")
                pass
            else:
                print("查询成功！以下是您的个人开户信息：")
                info = '''
                ----------个人信息------
                用户名：%s
                密码：%s
                身份证号：%s
                账号：%s
                地址信息
                国家：%s
                省份：%s
                街道：%s
                门牌号: %s
                余额：%s
                开户行地址：%s
                ------------------------
                '''
                print(info % (Bank.data_search(account_sch)[0], Bank.data_search(account_sch)[1], Bank.data_search(account_sch)[2],
                              Bank.data_search(account_sch)[3], Bank.data_search(account_sch)[4], Bank.data_search(account_sch)[5],
                              Bank.data_search(account_sch)[6], Bank.data_search(account_sch)[7], Bank.data_search(account_sch)[8],
                              Bank.data_search(account_sch)[9]))
        else:
            print("该用户不存在！")

    # 启动程序
    def start():
        while True:
            # 打印欢迎程序
            Bank.welcome()
            chose = input("请输入您的业务：")
            if chose == "1":
                Bank.addUser()
                pass
            elif chose == "2":
                Bank.savemoney()
                pass
            elif chose == "3":
                Bank.getmoney()
                pass
            elif chose == "4":
                Bank.trans()
                pass
            elif chose == "5":
                Bank.search()
                pass
            elif chose == "6":
                print("欢迎下次光临！")
                break
            else:
                print("输入错误！请重新输入！")


Bank.start()
