import time


# 登录页面操作逻辑
class LoginPage:
    def __init__(self, drive):
        self.driver = drive  # 将driver声明为全局变量

    def login(self, username, password):
        # 同意用户协议
        element = "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.TextView[3]"
        self.driver.find_element_by_xpath(element).click()
        time.sleep(5)
        # 点击登录按钮
        self.driver.find_element_by_id("com.sina.weibo:id/titleBack").click()
        time.sleep(2)
        # 切换到账号密码模式
        time.sleep(2)
        self.driver.find_element_by_id("com.sina.weibo:id/iv_psw").click()
        # 输入用户名
        self.driver.find_element_by_id("com.sina.weibo:id/et_login_view_uname").send_keys(username)
        # 输入密码
        self.driver.find_element_by_id("com.sina.weibo:id/et_login_view_psw").send_keys(password)
        # 同意用户协议
        self.driver.find_element_by_id("com.sina.weibo:id/iv_login_view_protocol").click()
        # 点击登陆
        self.driver.find_element_by_id("com.sina.weibo:id/btn_login_view_psw").click()

    def get_succes_data(self):
        try:
            data = self.driver.find_element_by_id("com.sina.weibo:id/titleLeft").text
        except Exception:
            data = self.driver.find_element_by_id("com.sina.weibo:id/tv_login_view_tips").text
        return data

    def get_error_data(self):
        try:
            data = self.driver.find_element_by_id("com.sina.weibo:id/tv_login_view_tips").text
        except Exception:
            data = self.driver.find_element_by_id("com.sina.weibo:id/titleLeft").text
        return data
