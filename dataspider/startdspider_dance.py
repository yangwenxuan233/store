from scrapy.cmdline import execute
# 导入cmdline模块,可以实现控制终端命令行。
import os  # 用来设置路径
import sys   # 调用系统环境，就如同cmd中执行命令一样

# 获取当前脚本路径
dirpath = os.path.dirname(os.path.abspath(__file__))
# 运行文件绝对路径
# print(os.path.abspath(__file__))
# 运行文件父路径
# print(dirpath)
# 添加环境变量
sys.path.append(dirpath)
# 切换工作目录
os.chdir(dirpath)


execute(['scrapy', 'crawl', 'testspider',
         '-a', 'type=舞蹈区', '-a',
         'start_url=https://www.bilibili.com/v/popular/rank/dance'])
