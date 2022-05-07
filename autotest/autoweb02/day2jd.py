from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get(r"http://www.jd.com")
driver.maximize_window()

time.sleep(2)

driver.find_element_by_link_text("你好，请登录").click()

time.sleep(2)

driver.find_element_by_link_text("账户登录").click()
driver.find_element_by_xpath('//*[@id="loginname"]').send_keys("17778885125")
driver.find_element_by_xpath('//*[@id="nloginpwd"]').send_keys("ywx690332516")
driver.find_element_by_xpath('//*[@id="loginsubmit"]').click()

time.sleep(5)

driver.find_element_by_link_text("房产").click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[1])

time.sleep(2)

driver.find_element_by_link_text('海淀区').click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[2])

time.sleep(2)

driver.find_element_by_link_text("10万元/㎡以上").click()
time.sleep(2)
driver.find_element_by_link_text(" 大苑·海淀府").click()

time.sleep(2)

driver.find_elements_by_id("InitCartUrl")

time.sleep(2)

driver.close()
