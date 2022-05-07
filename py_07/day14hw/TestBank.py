from unittest import TestCase
from ddt import ddt
from ddt import data
from ddt import unpack
from day6hw_ICBC_Bank import Bank
'''
    DDT:data driver test
        ddt
        data
        unpack
    1.测试类必须用@ddt修饰
    2.测试方法使用@data引入数据源
    任务：
        将工行系统的核心业务进行测试？
        bank_addUser()

'''
# 数据源
data_addUser = [
    [1, 1, 1, 12345678, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 87654321, 1, 1, 1, 1, 1, 2],
    [2, 2, 2, 12345678, 2, 2, 2, 2, 2, 2],
    [3, 3, 3, 66666666, 3, 3, 3, 3, 3, 1],
]


@ddt  # 注解，注释这个类是参数化类
class TestAddUser(TestCase):

    @data(*data_addUser)  # 引入数据源
    @unpack
    def testAdd(self, username, password, IDcard, account, country, province, street, gate, money, status):
        # 2.调用被测方法
        bank = Bank()
        result = bank.bank_addUser(username, password, IDcard, account, country, province, street, gate, money)
        # 3.断言
        self.assertEqual(result, status)


data_savemoney = [
    [12345678, 5, True],
    [66666666, 2, True],
    [12344321, 1, False],
]


@ddt
class TestSavemoney(TestCase):

    @data(*data_savemoney)
    @unpack
    def testSave(self, account_save, money_save, status):
        bank = Bank()
        result = bank.bank_savemoney(account_save, money_save)
        self.assertEqual(result, status)


data_getmoney = [
    [12345678, 1, 1, 0],
    [12344321, 1, 2, 1],
    [12345678, 2, 1, 2],
    [66666666, 3, 5, 3],
]


@ddt
class TestGetmoney(TestCase):

    @data(*data_getmoney)
    @unpack
    def testGet(self, account_get, password_get, money_get, status):
        bank = Bank()
        result = bank.bank_getmoney(account_get, password_get, money_get)
        self.assertEqual(result, status)


data_trans = [
    [12345678, 66666666, 1, 1, 0],
    [12345678, 33333333, 1, 1, 1],
    [22222222, 66666666, 1, 1, 1],
    [12345678, 66666666, 2, 1, 2],
    [12345678, 66666666, 1, 10, 3],
]


@ddt
class TestTrans(TestCase):

    @data(*data_trans)
    @unpack
    def testTrans(self, account_out, account_in, password_out, money_trans, status):
        bank = Bank()
        result = bank.bank_trans(account_out, account_in, password_out, money_trans)
        self.assertEqual(result, status)


data_search = [
    [12345678, 1, 0],
    [11111111, 1, 1],
    [66666666, 1, 2],
]


@ddt
class TestSearch(TestCase):

    @data(*data_search)
    @unpack
    def testSearch(self, account_sch, password_sch, status):
        bank = Bank()
        result = bank.bank_search(account_sch, password_sch)
        self.assertEqual(result, status)
