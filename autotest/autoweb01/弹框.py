# from selenium import webdriver
# import time
#
# driver = webdriver.Chrome()
#
#
# driver.get(r"F:\自动化测试11\day01\练习的html\练习的html\弹框的验证\dialogs.html")
# driver.maximize_window()
#
# driver.find_element_by_id("alert").click()
# time.sleep(1)
# driver.switch_to.alert.accept()  # accept 确定
#
#
#
#
# time.sleep(3)
# driver.quit()
#

from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get(r"D:\pycode\autoweb\autoweb01\练习的html\弹框的验证\dialogs.html")
driver.maximize_window()

driver.find_element_by_id("confirm").click()
time.sleep(1)
# driver.switch_to.alert.accept()  # accept 确定
driver.switch_to.alert.dismiss()  # 取消

time.sleep(3)
driver.quit()





