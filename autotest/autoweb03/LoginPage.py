'''
    就写登陆的页面的操作逻辑：


'''


class LoginPage:
    def __init__(self, drive):
        self.driver = drive  # 将driver生命为全局变量

    def login(self, username, password):
        # 输入用户名
        self.driver.find_element_by_xpath("//*[@id='loginname']").send_keys(username)
        # 输入密码
        self.driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
        # 点击登陆
        self.driver.find_element_by_xpath("//*[@id='submit']").click()

    def get_succes_data(self):
        return self.driver.title

    def get_error_data(self):
        return self.driver.find_element_by_xpath("//*[@id='msg_uname']").text
