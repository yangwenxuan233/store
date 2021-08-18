from appium import webdriver
import time


class autodouyin():

    driver = None

    def auto_swipe(self):
        server = r'http://localhost:4723/wd/hub'  # Appium Server, 端口默认为4723
        desired_capabilities = {
            'platformName': 'Android',  # 平台
            'deviceName': '127.0.0.1:21503',  # 逍遥模拟器端口21503、夜神62001、雷电5555
            'platformVersion': '7.1.2',  # 安卓版本
            'appPackage': 'com.ss.android.ugc.aweme',  # APP包名
            'appActivity': 'com.ss.android.ugc.aweme.splash.SplashActivity',  # APP启动名
            'noReset': True,
            'unicodeKeyboard': True,  # 这句和下面那句是避免中文问题的
            'resetKeyboard': True
        }
        self.driver = webdriver.Remote(server, desired_capabilities)  # 连接手机和APP
        time.sleep(3)  # 等待app启动
        while True:
            try:
                time.sleep(2)
                self.swipe_up()
            except Exception as e:
                print(str(e))
                break
        self.driver.quit()  # 退出driver

    def swipe_up(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(x*0.5, y*0.75, x*0.5, y*0.25)


d = autodouyin()
d.auto_swipe()
