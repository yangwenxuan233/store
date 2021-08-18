'''
    dirver:
        点击
        输入数据
    面试题：窗口切换：
        获取窗口句柄，switch_to.window()
    面试题2:
        为啥窗口最大化？
        有的元素就没法定位！
    面试题3：
        定位有几种？
            8
        定位不到什么问题？
            1.窗口最大化？
                最大化
            2.id号是不是动态变化？
                可以通过赛选进行精确定位
            3.页面没有渲染完成，就开始定位
                time.sleep(2)
            4.有的元素在获取就不是一个
                [0]

    实现京东登陆，买个东西加入购物车，结算。
    淘宝登陆，买个东西加入购物车。
    苏宁无登陆，登陆情况，添加购物车，结算。




'''
from selenium import  webdriver
import time
driver = webdriver.Chrome()

driver.get("https://www.jd.com")
driver.maximize_window()

# 定义我的订单
driver.find_element_by_link_text("我的订单").click()

# 窗口切换

# 获取所有窗口的句柄
data = driver.window_handles


driver.switch_to.window(data[1])  # 切换窗口


# 点击账户登陆
driver.find_element_by_link_text("账户登录").click()

# 输入用户名
driver.find_element_by_xpath("//*[@id='loginname']").send_keys("jason")
# 输入密码
driver.find_element_by_xpath("//*[@id='nloginpwd']").send_keys("123jqrioautdqpoewriodqhsmriero")

# 点击登陆
driver.find_element_by_xpath("//*[@id='loginsubmit']").click()

# 挺
time.sleep(3)

driver.quit()

















