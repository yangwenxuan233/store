users = {'User':'xiaoming', 'Psw':'123456'}
class UsersBiz(object):
    def __init__(self, User= '', Psw= ''):
        self.User = User
        self.Psw = Psw
        pass
    def login(self):
        for i in range(3):
            self.User = input("请输入用户名：")
            self.Psw = input("请输入密码：")
            j = 2-i
            if self.User == '' or self.Psw == '':
                print("输入不能为空！")
                print("还有" + str(j)+'次机会！')
                pass
            elif self.User != users['User'] or self.Psw != users['Psw']:
                print("账号或密码输入有误！")
                print("还有" + str(j)+'次机会！')
                pass
            else:
                print("账号密码输入正确!")
                break
                pass
        pass
    pass

User1 = UsersBiz('xiaoming', '123456')
User1.login()






