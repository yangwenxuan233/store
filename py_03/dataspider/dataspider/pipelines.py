# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DataspiderPipeline:
    def process_item(self, item, spider):
        print(item['job_name'], end="\t")
        print(item['job_company'], end="\t")
        print(item['job_salary'], end="\t")
        print(item['job_address'], end="\t")
        print(item['job_date'], end="\n")
        print(item['job_info'], end="\n")

        # 数据采集  数据处理 数据的存储（数据库） 数据分析（普通和机器学习）和可视化

        return item
