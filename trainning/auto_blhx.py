from appium import webdriver
import time


class Autoblhx():

    driver = None

    def start(self):
        server = r'http://localhost:4723/wd/hub'  # Appium Server, 端口默认为4723
        desired_capabilities = {
            'platformName': 'Android',  # 平台
            'deviceName': '127.0.0.1:21503',  # 逍遥模拟器端口21503、夜神62001、雷电5555
            'platformVersion': '7.1.2',  # 安卓版本
            'appPackage': 'com.bilibili.azurlane',  # APP包名
            'appActivity': 'com.manjuu.azurlane.MainActivity',  # APP启动名
            'noReset': True,
            'unicodeKeyboard': True,  # 这句和下面那句是避免中文问题的
            'resetKeyboard': True
        }
        self.driver = webdriver.Remote(server, desired_capabilities)  # 连接手机和APP
        time.sleep(50)  # 等待app启动

        # 触屏进入
        self.driver.tap([(1200, 300)], 500)
        time.sleep(5)
        # 关闭系统公告
        self.driver.tap([(1200, 78)], 500)
        time.sleep(3)
        # 点击出击
        self.driver.tap([(1062, 383)], 500)
        time.sleep(3)
        # 选择模式
        self.driver.tap([(750, 232)], 500)
        time.sleep(3)
        # 选择关卡
        self.driver.tap([(680, 590)], 500)
        time.sleep(3)
        # 立刻前往
        self.driver.tap([(950, 520)], 500)
        time.sleep(3)
        self.driver.tap([(1070, 600)], 500)
        time.sleep(30)
        # 重复再次前往
        for i in range(60):
            try:
                self.driver.tap([(840, 620)], 500)
                time.sleep(1)
                self.driver.tap([(890, 200)], 500)
                time.sleep(30)
            except Exception as e:
                print(str(e))
                break
        time.sleep(30)
        self.driver.quit()  # 退出driver


rua = Autoblhx()
rua.start()
