'''
    定位：
        id
        xpath
    任务1：将点击弹框任务脚本写出来
    任务2：第二项


'''

from selenium import webdriver
import time

driver = webdriver.Chrome()


driver.get(r"D:\pycode\autoweb\autoweb01\练习的html\上传文件和下拉列表\autotest.html")
driver.maximize_window()

# 1.输入用户名
# driver.find_element_by_id("accountID")
driver.find_element_by_xpath("//*[@id='accountID' and @name='account' and @type='text']").send_keys("jason")
# 2.输入密码
driver.find_element_by_xpath("//*[@id='passwordID']").send_keys("102775")

# 3.下拉
driver.find_element_by_xpath("//*[@id='areaID']").send_keys("北京市")

# 4.性别
driver.find_element_by_xpath("//*[@id='sexID2']").click()
# 季节
driver.find_element_by_xpath("//*[@value='spring']").click()
driver.find_element_by_xpath("//*[@value='Auterm']").click()

# 6.上传文件
driver.find_element_by_xpath("//*[@name='file' and @type='file']").send_keys(r"D:\pycode\py202107\day15hw\day15\大美女.jpg")

time.sleep(3)
driver.quit()
