from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get(r"D:\pycode\autoweb\autoweb01\练习的html\跳转页面\pop.html")

driver.maximize_window()

driver.find_element_by_xpath("//*[@id='goo']").click()

time.sleep(10)

driver.close()
