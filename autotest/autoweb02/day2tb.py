from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
import time

# 淘宝
driver = webdriver.Chrome()
driver.get(r"http://www.taobao.com")
driver.maximize_window()

driver.find_element_by_link_text('亲，请登录').click()

time.sleep(2)

driver.find_element_by_id("fm-login-id").send_keys("17778885125")
driver.find_element_by_id("fm-login-password").send_keys("ywx690332516")
driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()

# ac = ActionChains(driver)
# ele = driver.find_element_by_xpath('//*[@id="nc_2_n1z"]')
# ac.click_and_hold(ele).move_by_offset(300, 0).perform()

time.sleep(2)

driver.find_element_by_link_text('打火机').click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[1])

driver.find_element_by_link_text('2019年秋季').click()
driver.find_element_by_xpath('//*[@id="mx_5"]/ul/li[4]/a/img').click()

time.sleep(2)

handle = driver.window_handles
driver.switch_to.window(handle[2])

driver.find_element_by_xpath('//*[@id="mx_9"]/div/div/a/img').click()

time.sleep(2)

driver.find_element_by_id('J_LinkBasket').click()
driver.find_element_by_link_text('赛博霓虹').click()
driver.find_element_by_link_text('确认').click()

time.sleep(2)

driver.close()
