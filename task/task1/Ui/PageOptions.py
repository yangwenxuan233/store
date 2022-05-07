class BuyMoistrurizers:
    def __init__(self, drive):
        self.driver = drive

    def buy_moisturizers(self, path):
        # enter page
        self.driver.find_element_by_xpath("/html/body/div/div[3]/div[1]/a/button").click()
        # choose product
        self.driver.find_element_by_xpath(path).click()

    def get_succes_data(self):
        pass

    def get_failed_data(self):
        pass


class BuySunscreens:
    def __init__(self, drive):
        self.driver = drive

    def buy_sunscreens(self, path):
        # enter page
        self.driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/a/button").click()
        # choose product
        self.driver.find_element_by_xpath(path).click()

    def get_succes_data(self):
        pass

    def get_failed_data(self):
        pass
