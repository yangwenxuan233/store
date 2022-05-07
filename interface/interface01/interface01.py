import re
import requests
import xlwt
import datetime
# from lxml import etree


class Weather():

    name_list = []
    time = ""

    # 修改名称列表
    def setNamelist(self, list):
        self.name_list = list

    # 获取网页文本信息
    def get_html(self, name):
        url = 'http://flash.weather.com.cn/wmaps/xml/%s.xml' % name
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        response = requests.get(url, headers=header)
        response.encoding = 'utf-8'
        html = response.text
        return html

    # 对网页文本信息进行过滤
    def get_data(self, name):
        html = self.get_html(name)
        try:
            rows = html.split(">")
            data = []
            for i in rows:
                row = re.findall(r"['\"](.*?)['\"]", i)
                if len(row) > 1:
                    data.append(row)
        except Exception as e:
            print(str(e))
        return data

    # 数据逐行写入excel表格
    def datashow_excel(self):
        # 新建表格
        workbook = xlwt.Workbook(encoding='utf8')
        # 写入数据
        for name in self.name_list:
            sheet = workbook.add_sheet(name)
            data = self.get_data(name)
            row = 0
            for i in data:
                for key, value in enumerate(i):
                    sheet.write(row, key, value)
                row = row + 1
            # 设置长字符列宽
            sheet.col(5).width = 256 * 12
            sheet.col(8).width = 256 * 12
            sheet.col(12).width = 256 * 20
            # 按当前日期命名保存
            workbook.save("%s.xlsx" % self.time)

    # 获取当天日期
    def get_time(self):
        self.time = str(datetime.date.today())

    # 启动
    def main(self, list):
        try:
            self.setNamelist(list)
            self.get_time()
            self.datashow_excel()
            print("数据获取完成")
        except Exception as e:
            print(str(e))


name_list = [
    'china',
    'beijing', 'shanghai', 'tianjin', 'chongqing', 'xianggang',
    'aomen', 'anhui', 'fujian', 'guangdong', 'guangxi',
    'guizhou', 'gansu', 'hainan', 'hebei', 'henan',
    'heilongjiang', 'hubei', 'hunan', 'jilin', 'jiangsu',
    'jiangxi', 'liaoning', 'neimenggu', 'ningxia', 'qinghai',
    'shanxi', 'sanxi',  'shandong', 'sichuan', 'taiwan',
    'xizang', 'xinjiang', 'yunnan', 'zhejiang'
]

w = Weather()
w.main(name_list)
