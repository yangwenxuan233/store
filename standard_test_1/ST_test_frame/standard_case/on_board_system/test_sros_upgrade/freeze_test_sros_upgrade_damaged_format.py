# -*- coding: utf-8 -*-
"""
@Author: ywx
@Date: 2022-3-21
@Modify:
@Modify Date:
@Description: abandoned
"""

import time
import unittest
from pathlib import Path


import ddt
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings


@ddt.ddt
class TestUpgrade(unittest.TestCase):
    '''SROS系统固件升级用例, 固件格式损坏升级。
    '''

    def setUp(self) -> None:
        '''用例初始化, 开启日志模块。
        '''
        self.logger = Logs()
        self.driver = webdriver.Chrome()

    def tearDown(self) -> None:
        '''用例结束处理, 清除日志模块句柄。
        '''
        self.logger.logger.handlers.pop()
        time.sleep(2)
        self.driver.close()

    @ddt.file_data(settings.BOARD_YAML)
    def test_upgrade_fail(self, **kwargs):
        """验证类型: 异常, 用例标题: 固件格式损坏升级, 预期结果: 升级失败, 是否冒烟: 是。
        """
        self.ip = kwargs['ip']
        self.base_path = Path(settings.YAML_PATH)
        self.firmware_name = kwargs['sros_name'][3]
        self.username = kwargs['login']['username']
        self.password = kwargs['login']['password']
        self.firmware_path = list(self.base_path.glob(f"**/{self.firmware_name}"))[0]
        self.assertIsNotNone(self.firmware_path)
        self.logger.info(self.firmware_path)
        self.driver.get('http:/' + self.ip)
        self.driver.maximize_window()
        # 设置显式等待时长
        wait = WebDriverWait(self.driver, 5)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="background"]/div/div/div[3]/div[2]/div/div/div/div[1]/label[2]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="background"]/div/div/div[3]/div[2]/div/div/div/div[2]/label[2]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="background"]/div/div/div[3]/div[2]/div/div/div/button/span[2]/span').click()
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listMenus"]/a[6]/div[2]/div/div')))
        element.click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="q-app"]/div/div[2]/main/div/div/div/div[9]/div/button[1]/span[2]/span/div').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/button/span[2]/span/div').click()
        time.sleep(0.25)
        pyautogui.typewrite(str(self.firmware_path))
        pyautogui.press('enter')
        result = self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[4]/button[1]/span[2]/span/div').text
        self.logger.info(result)
        self.assertEqual('取消', result)


if __name__ == '__main__':
    unittest.main()
