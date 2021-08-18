import scrapy
import requests
import json
import re
from lxml import etree
from ..items import DataspiderItem


class TestspiderSpider(scrapy.Spider):
    name = 'testspider'
    start_urls = []
    # 使用xpath解析，也可以使用bs等其他的方式
    # urls = ["https://www.bilibili.com/v/popular/rank/douga", "https://www.bilibili.com/v/popular/rank/guochuang"]

    def __init__(self, type, start_url, *args, **kw):
        super(TestspiderSpider, self).__init__(*args, **kw)
        TestspiderSpider.base_url = start_url
        TestspiderSpider.start_urls.append(start_url.format(1))

        self.type = type
        pass

    def parse(self, response):
        html = etree.HTML(response.text)
        title = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li//div[@class="info"]/a/text()')
        playVolume = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li//div[@class="info"]//div[@class="detail"]/span[1]/text()')
        barrage = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li//div[@class="info"]//div[@class="detail"]/span[2]/text()')
        overallRatings = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li//div[@class="info"]//div[@class="pts"]/div/text()')
        author = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li//div[@class="info"]//span[@class="data-box up-name"]/text()')
        rank = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li[@class="rank-item"]/div[@class="num"]/text()')
# a[@href]
        # //*[@id="app"]/div[2]/div[2]/ul/li[2]/div[2]/div[2]/a
        link = html.xpath(
            '//div[@class="rank-container"]/div[@class="rank-list-wrap"]/ul/li//div[@class="info"]/a/@href')
        # print(title)
        # print(playVolume)
        # print(barrage)
        # print(overallRatings)
        # print(author)
        # print(rank)

        for t, p, b, o, a, r, l in zip(title, playVolume, barrage, overallRatings, author, rank, link):
            pipeItem = DataspiderItem()
            pipeItem['title'] = str(t).strip()
            pipeItem['title'] = re.sub('\\[.*?\\]', '', pipeItem['title'])
            pipeItem['playVolume'] = str(p).strip()
            pipeItem['barrage'] = str(b).strip()
            pipeItem['overallRatings'] = str(o).strip()
            pipeItem['author'] = str(a).strip()
            pipeItem['rank'] = str(r).strip()
            pipeItem['link'] = "https:" + str(l).strip()
            pipeItem['type'] = self.type
            # like_on = pipeItem['link'].xpath(
            #     '//div[@class="ops"]/text()')
            # self.second_url.append(nexturl)
            # print(nexturl)
            if len(link) > 0:
                request = scrapy.Request(pipeItem['link'])
                request.callback = self.parse_second_page
                request.meta['pipeItem'] = pipeItem
                yield request

            # yield scrapy.Request(url=second_page, callback=self.parse_second_page, meta={'pipeItem': pipeItem} ,dont_filter=True)
            yield pipeItem

    def parse_second_page(self, response):
        # 编写采集二级页面的实现
        pipeItem = response.meta['pipeItem']
        pipeItem['like_on'] = response.xpath('//div[@class="ops"]/span[1]/text()')[0].extract().strip()
        pipeItem['coin_on'] = response.xpath('//div[@class="ops"]/span[2]/text()')[0].extract().strip()
        pipeItem['collect_on'] = response.xpath('//div[@class="ops"]/span[3]/text()')[0].extract().strip()
        yield pipeItem
