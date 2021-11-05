# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    job_company= scrapy.Field()
    job_address = scrapy.Field()
    job_salary = scrapy.Field()
    job_date = scrapy.Field()
    job_url = scrapy.Field()
    job_type = scrapy.Field()
    job_info = scrapy.Field()
    pass
