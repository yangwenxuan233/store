from unittest import TestCase
from appium import webdriver
from ddt import ddt
from ddt import data
# from ddt import unpack
from Initpage import Initpage  # 页面的数据
from LoginPage import LoginPage  # 页面的操作逻辑
import time


@ddt
class TestLogin(TestCase):

    server = r'http://localhost:4723/wd/hub'  # Appium Server, 端口默认为4723
    desired_capabilities = {
        'platformName': 'Android',  # 平台
        'deviceName': '127.0.0.1:21503',  # 逍遥模拟器端口21503、夜神62001、雷电5555
        'platformVersion': '7.1.2',  # 安卓版本
        'appPackage': 'com.sina.weibo',  # APP包名
        'appActivity': 'com.sina.weibo.SplashActivity',  # APP启动名
        # 'noReset': True,
        'unicodeKeyboard': True,  # 这句和下面那句是避免中文问题的
        'resetKeyboard': True
    }

    # 在每个操作之前先做预备工作
    def setUp(self) -> None:
        self.imgs = []
        self.driver = webdriver.Remote(self.server, self.desired_capabilities)  # 连接手机和APP
        time.sleep(3)  # 等待app启动

    # 在每个用例执行后，将app关闭
    def tearDown(self) -> None:
        time.sleep(2)
        self.driver.quit()  # 退出app

    # 登陆成功用例
    @data(*Initpage.login_success_data)
    def testLoginsuccess(self, testdata):
        # 提取用户名，密码，期望结果
        username = testdata["username"]
        password = testdata["password"]
        expect = testdata["expect"]

        login = LoginPage(self.driver)
        login.login(username, password)

        #  获取实际结果
        result = login.get_succes_data()
        time.sleep(1)
        if result != expect:
            self.imgs.append(self.driver.get_screenshot_as_base64())
        # 断言
        self.assertEqual(expect, result)

    # 登录失败的用例
    @data(*Initpage.login_error_data)
    def testLoginerror(self, testdata):
        # 提取用户名，密码，期望结果
        username = testdata["username"]
        password = testdata["password"]
        expect = testdata["expect"]

        login = LoginPage(self.driver)
        login.login(username, password)

        # 获取实际结果
        result = login.get_error_data()
        time.sleep(1)

        # 与预期结果不符则截图
        if result != expect:
            self.imgs.append(self.driver.get_screenshot_as_base64())
        # 断言
        self.assertEqual(expect, result)
