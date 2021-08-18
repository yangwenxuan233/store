'''
    中国工商银行账户管理系统：
        ICBC:
'''
import random
# import hashlib


class Bank():
    # 准备一个数据库 和 银行名称
    bank = {}  # 空的数据库
    user = {}  # 空的用户数据表 username和IDcard为双主键
    bank_name = "中国工商银行昌平回龙观支行"  # 银行名称写死的

    '''
    # 加密
    def md5(str):
        m = hashlib.md5()
        m.update(str.encode("utf8"))
        return m.hexdigest()
    '''

    # 入口程序
    def welcome():
        if __name__ == "__main__":
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
    def bank_addUser(self, username, password, IDcard, account, country, province, street, gate, money):
        # 1.判断数据库是否已满
        if len(self.bank) >= 100:
            return 3
        # 2.判断用户是否存在
        if (username, IDcard) in self.user or account in self.bank:
            return 2
        # 3.正常开户
        self.bank[account] = {
            "username": username,
            "password": password,
            "IDcard": IDcard,
            "account": account,
            "country": country,
            "province": province,
            "street": street,
            "gate": gate,
            "money": money,
            "bank_name": self.bank_name
        }
        self.user[(username, IDcard)] = account
        return 1

    # 用户的开户的操作逻辑
    def addUser(self):
        if __name__ == "__main__":
            username = input("请输入您的用户名：")
            password = int(input("请输入您的开户密码："))
            IDcard = input("请输入您的身份证号：")
            account = random.randint(10000000, 99999999)  # 随机产生8为数字
            country = input("请输入您的国籍：")
            province = input("请输入您的居住省份：")
            street = input("请输入您的街道：")
            gate = input("请输入您的门牌号：")
            money = int(input("请输入您的开户初始余额："))  # 将输入金额转换成int类型

            status = Bank.bank_addUser(username, password, IDcard, account, country, province, street, gate, money)

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
                print(info % (username, IDcard, account, password, country, province, street, gate, money, self.bank_name))

    # 存钱逻辑
    def bank_savemoney(self, account_save, money_save):
        if account_save not in self.bank:
            return False
        else:
            self.bank[account_save]["money"] = self.bank[account_save]["money"] + money_save
            return True

    # 存钱操作逻辑
    def savemoney(self):
        if __name__ == "__main__":
            account_save = int(input("请输入您的账号:"))
            money_save = int(input("请输入您的存款金额:"))
            status = self.bank_savemoney(account_save, money_save)
            if status:
                print("存钱成功！当前余额：", self.bank[account_save]["money"])
                pass
            else:
                print("该用户不存在！")
                pass

    # 取钱逻辑
    def bank_getmoney(self, account_get, password_get, money_get):
        if account_get not in self.bank:
            return 1
        elif password_get != self.bank[account_get]["password"]:
            return 2
        elif money_get > self.bank[account_get]["money"]:
            return 3
        else:
            self.bank[account_get]["money"] = self.bank[account_get]["money"] - money_get
            return 0

    # 取钱操作逻辑
    def getmoney(self):
        if __name__ == "__main__":
            account_get = int(input("请输入您的账号："))
            password_get = int(input("请输入您的密码："))
            money_get = int(input("请输入您的取款金额："))
            status = self.bank_getmoney(account_get, password_get, money_get)
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
                print("取款成功！当前余额：", self.bank[account_get]["money"])
                pass

    # 转账逻辑
    def bank_trans(self, account_out, account_in, password_out, money_trans):
        if any([account_out not in self.bank, account_in not in self.bank]):
            return 1
        elif password_out != self.bank[account_out]["password"]:
            return 2
        elif money_trans > self.bank[account_out]["money"]:
            return 3
        else:
            self.bank[account_in]["money"] = self.bank[account_in]["money"] + money_trans
            self.bank[account_out]["money"] = self.bank[account_out]["money"] - money_trans
            return 0

    # 转账操作逻辑
    def trans(self):
        if __name__ == "__main__":
            account_out = int(input("请输入您要转出的账号："))
            account_in = int(input("请输入您要转入的账号："))
            password_out = int(input("请输入您要转出的密码："))
            money_trans = int(input("请输入您要转出的金额："))
            status = self.bank_trans(account_out, account_in, password_out, money_trans)
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
                print("转出账户余额：", self.bank[account_out]["money"])
                print("转入账户余额：", self.bank[account_in]["money"])
                pass

    # 查询账户逻辑
    def bank_search(self, account_sch, password_sch):
        if account_sch in self.bank:
            if password_sch != self.bank[account_sch]["password"]:
                return 2
            else:
                return 0
        else:
            return 1
    # 查询操作逻辑

    def search(self):
        if __name__ == "__main__":
            account_sch = int(input("请输入您要查询的账号："))
            password_sch = int(input("请输入您要查询的密码："))
            status = Bank.bank_search(account_sch, password_sch)
            if status == 2:
                print("密码错误！")
                pass
            elif status == 0:
                print("查询成功！以下是您的个人开户信息：")
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
                print(info % (self.bank[account_sch]["username"], self.bank[account_sch]["IDcard"], self.bank[account_sch]["account"],
                              self.bank[account_sch]["password"], self.bank[account_sch]["country"], self.bank[account_sch]["province"],
                              self.bank[account_sch]["street"], self.bank[account_sch]["gate"], self.bank[account_sch]["money"],
                              self.bank[account_sch]["bank_name"]))
            else:
                print("用户不存在！")

    def start(self):
        if __name__ == "__main__":
            while True:
                # 打印欢迎程序
                self.welcome()
                chose = input("请输入您的业务：")
                if chose == "1":
                    self.addUser()
                    pass
                elif chose == "2":
                    self.savemoney()
                    pass
                elif chose == "3":
                    self.getmoney()
                    pass
                elif chose == "4":
                    self.trans()
                    pass
                elif chose == "5":
                    self.search()
                    pass
                elif chose == "6":
                    print("欢迎下次光临！")
                    break
                else:
                    print("输入错误！请重新输入！")
