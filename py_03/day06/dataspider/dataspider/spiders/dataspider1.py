import scrapy


class Dataspider1Spider(scrapy.Spider):
    name = 'dataspider1'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
