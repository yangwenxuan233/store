from selenium import webdriver
import time

driver = webdriver.Chrome()


driver.get(r"D:\pycode\autoweb\autoweb01\练习的html\frame.html")
driver.maximize_window()


# 定位
driver.find_element_by_id("input1").send_keys("hello,jason!来了老弟！")


time.sleep(3)
driver.quit()















