# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    playVolume = scrapy.Field()
    barrage = scrapy.Field()
    overallRatings = scrapy.Field()
    author = scrapy.Field()
    rank = scrapy.Field()
    link = scrapy.Field()
    like_on = scrapy.Field()
    coin_on = scrapy.Field()
    collect_on = scrapy.Field()
    type = scrapy.Field()

    pass
