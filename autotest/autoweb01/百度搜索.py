from selenium import webdriver
import time
# 创建驱动
driver = webdriver.Chrome()


# 打开一个网址
driver.get("http://www.baidu.com")
# 最大化
driver.maximize_window()

#  定义输入框
driver.find_element_by_id("kw").send_keys("helloWorld!") # 输入数据

# 定位按钮
driver.find_element_by_id("su").click() # 点击


#  停3秒
time.sleep(3)
driver.quit() # 关闭浏览器
























