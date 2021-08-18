from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
import time

# 苏宁
driver = webdriver.Chrome()
driver.get(r"http://www.suning.com")
driver.maximize_window()

driver.find_element_by_name("utf-8_homepagev8_126605238671_word01").click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[1])

driver.find_element_by_name('pindao_wan3C_127216015284_word03').click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[2])

driver.find_element_by_name('ssdln_20006_gjsx_价格-8000以上').click()
time.sleep(2)
driver.find_element_by_name('ssdln_20006_pro_name03-1_0_0_12174647278_0070094634').click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[3])

driver.find_element_by_id('addCart').click()

time.sleep(2)

driver.close()
