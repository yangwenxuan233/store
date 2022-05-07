from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get(r"http://localhost:8080/HKR")

# 登录
driver.find_element_by_xpath("//*[@id='loginname' and @name='loginname']").send_keys("root")
driver.find_element_by_xpath("//*[@id='password' and @name='password']").send_keys("root")
driver.find_element_by_xpath("//*[@id='submit' and @value='登陆']").click()

time.sleep(2)

# 提交今日评价
driver.find_element_by_xpath("//*[@name='time' and @class='show_tea']").send_keys('9（上晚自习）')
driver.find_element_by_xpath("//*[@name='teaName' and @class='show_tea']").send_keys('贾生')
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[5]/td[3]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[6]/td[2]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[7]/td[3]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[8]/td[2]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[9]/td[2]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[10]/td[3]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[11]/td[2]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@name='formtable']/tbody/tr[12]/td[2]/div/label[1]/div").click()
driver.find_element_by_xpath("//*[@id='textarea' and @name='suggestion']").send_keys("无")
time.sleep(1)
driver.find_element_by_xpath("//*[@id='subtn']").click()
try:
    driver.find_element_by_xpath("/html/body/div[7]/div[3]/a").click()
except Exception:
    driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[2]/a").click()

time.sleep(2)

# 修改个人信息
driver.refresh()
driver.find_element_by_xpath('//*[@id="_easyui_tree_8"]/span[4]/a').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[1]/td[2]/input').clear()
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[1]/td[2]/input').send_keys("root")
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[3]/td[2]/input').clear()
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[3]/td[2]/input').send_keys("root")
driver.find_element_by_xpath('//*[@id="_easyui_textbox_input1"]').clear
driver.find_element_by_xpath('//*[@id="_easyui_textbox_input1"]').send_keys("女")
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[6]/td[2]/input').clear()
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[6]/td[2]/input').send_keys("北京市")
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[8]/td[2]/input').clear()
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[8]/td[2]/input').send_keys('13552648187@qq.com')
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[9]/td[2]/textarea').clear()
driver.find_element_by_xpath('//*[@id="info"]/table/tbody/tr[9]/td[2]/textarea').send_keys('那咋办嘛')
driver.find_element_by_xpath('//*[@id="btn_modify"]').click()

time.sleep(2)

# 查看所有好友
driver.refresh()
driver.find_element_by_xpath('//*[@id="_easyui_tree_10"]/span[4]/a').click()

time.sleep(2)

# 关于狼腾测试员
driver.refresh()
driver.find_element_by_xpath('//*[@id="_easyui_tree_12"]/span[4]/a').click()

time.sleep(2)

# 更换头像
driver.refresh()
driver.find_element_by_xpath('//*[@id="img"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="file1"]').send_keys(r"D:\pycode\py202107\day15hw\day15\大美女.jpg")
driver.find_element_by_xpath('//*[@id="pic_btn"]').click()

time.sleep(2)

# 退出登录
driver.find_element_by_xpath('//*[@id="top"]/div/a[2]/img').click()

time.sleep(2)

# 退出系统
driver.close()
