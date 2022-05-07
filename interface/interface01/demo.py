import requests
import re
import datetime
# from bs4 import BeautifulSoup


url = 'http://flash.weather.com.cn/wmaps/xml/china.xml'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
response = requests.get(url, headers=header)
code = response.apparent_encoding
response.encoding = code
html = response.content.decode(code)
# soup = BeautifulSoup(html, 'html.parser')
# list = soup.find_all()
# print(list)
html = response.text
rows = html.split(">")
list = []
for i in rows:
    row = re.findall(r"['\"](.*?)['\"]", i)
    if len(row) > 1:
        list.append(row)
print(list)
now_time = datetime.date.today()
print(str(now_time))
