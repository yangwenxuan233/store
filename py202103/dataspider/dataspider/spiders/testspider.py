import scrapy
import json
from day06.dataspider.dataspider.items import DataspiderItem

# 爬虫程序，其实就是模拟浏览器功能
class TestspiderSpider(scrapy.Spider):
    name = 'testspider'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=']  # http

    base_url = "https://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,{0}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    page_no = 1
    # 会将返回的response交给parse函数处理，返回的数据（html页面、json）会封装在response对象里
    def parse(self, response):
        print("爬虫程序启动成功:")  # xpath解析   bs4
        # print(response.text)
        items = response.xpath('//script[@type="text/javascript"]/text()') # 返回的是选择器对象

        for item in items:
            jsonText = item.extract() # extract函数 解析出选择器对象里的文本内容
            if jsonText.find("__SEARCH_RESULT__") > 0:
                jobsText = jsonText.split("__SEARCH_RESULT__ =")[1]
                # print(jobsText) # 把文本格式的json转成python
                jobsDict = json.loads(jobsText)['engine_search_result']

                for jobItem in  jobsDict:
                    second_page = jobItem['job_href']
                    # 管道对象
                    pipeItem = DataspiderItem()

                    # 封装管道数据
                    pipeItem['job_name'] = jobItem['job_name']
                    pipeItem['job_company'] = jobItem['company_name']
                    pipeItem['job_address'] = jobItem['workarea_text']
                    pipeItem['job_salary'] = jobItem['providesalary_text']
                    pipeItem['job_date'] = jobItem['updatedate']
                    pipeItem['job_url'] = jobItem['job_href']

                    # 采集二级页面，得到二级页面的地址
                    yield scrapy.Request(url=second_page, callback=self.parse_second_page, meta={'pipeItem': pipeItem} ,dont_filter=True)
                    pass
                pass
            pass

        # 处理解析下一页的方式
        TestspiderSpider.page_no += 1
        next_url = TestspiderSpider.base_url.format(TestspiderSpider.page_no)
        yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)

        pass

    def parse_second_page(self, response):
        # 编写采集二级页面的实现
        pipItem = response.meta['pipeItem']
        info = response.xpath("//div[@class='bmsg job_msg inbox']")
        if info:
            # print(info[0].extract())
            pipItem['job_info'] = info[0].extract()
            yield pipItem  # 向管道输出数据
            pass
        pass

    # 晚上的作业就是完成下午讲的内容，自己参考实现。
