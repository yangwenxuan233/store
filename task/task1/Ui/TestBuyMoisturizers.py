import time
from unittest import TestCase

from ddt import data, ddt
from selenium import webdriver

from Initpage import Initpage
from PageOptions import BuyMoistrurizers


@ddt
class TestBuyMoisturizers(TestCase):

    def setUp(self) -> None:
        self.imgs = []
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://weathershopper.pythonanywhere.com/")
        time.sleep(2)

    def tearDown(self) -> None:
        time.sleep(2)
        self.driver.quit()

    @data(*Initpage.moisturizers_data)
    def test_moistrurizers_success(self, testdata):
        # get data
        xpath = testdata["xpath"]
        expect = testdata["expect"]

        # pass data to do options
        option = BuyMoistrurizers(self.driver)
        option.buy_moisturizers(xpath)

        # get result
        result = option.get_succes_data()
        # get error screenshot
        if result != expect:
            self.imgs.append(self.driver.get_screenshot_as_base64())
        # assert
        self.assertEqual(expect, result)

    @data(*Initpage.moisturizers_data)
    def test_moistrurizers_failed(self, testdata):
        # get data
        xpath = testdata["xpath"]
        expect = testdata["expect"]

        # pass data to do options
        option = BuyMoistrurizers(self.driver)
        option.buy_moisturizers(xpath)

        # get result
        result = option.get_failed_data()
        # get error screenshot
        if result != expect:
            self.imgs.append(self.driver.get_screenshot_as_base64())
        # assert
        self.assertEqual(expect, result)
