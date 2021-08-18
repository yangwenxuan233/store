from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 事件链
import time
driver = webdriver.Chrome()

driver.get("https://www.qcc.com")
driver.maximize_window()

# 点击登录 | 注册
driver.find_element_by_link_text("登录 | 注册").click()


'''
    委托模型：
        将driver对象交个actionchains帮你管理
'''
ac = ActionChains(driver)  # 事件链对象

time.sleep(3)
ele = driver.find_element_by_xpath("//*[@id='nc_1_n1z']")

time.sleep(2)
ac.click_and_hold(ele).move_by_offset(348, 0).perform()  # 立即执行

time.sleep(3)
driver.quit()
