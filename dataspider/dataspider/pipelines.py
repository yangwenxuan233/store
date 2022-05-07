# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
from .dao.bilibilidao import JobDao


class DataspiderPipeline:
    def process_item(self, item, spider):

        if item['playVolume'].find("万") > 0:
            playVolumeStr = item['playVolume'].split('万')[0]
            if playVolumeStr.find("-") > 0:
                salaryArray = playVolumeStr.split('-')
                item['playVolume'] = float(salaryArray[0]) * 10000

        if item['like_on'].find("万") > 0:
            playVolumeStr = item['like_on'].split('万')[0]
            if playVolumeStr.find("-") > 0:
                salaryArray = playVolumeStr.split('-')
                item['like_on'] = float(salaryArray[0]) * 10000

        if item['coin_on'].find("万") > 0:
            playVolumeStr = item['coin_on'].split('万')[0]
            if playVolumeStr.find("-") > 0:
                salaryArray = playVolumeStr.split('-')
                item['coin_on'] = float(salaryArray[0]) * 10000

        if item['collect_on'].find("万") > 0:
            playVolumeStr = item['collect_on'].split('万')[0]
            if playVolumeStr.find("-") > 0:
                salaryArray = playVolumeStr.split('-')
                item['collect_on'] = float(salaryArray[0]) * 10000

        if item['barrage'].find("万") > 0:
            playVolumeStr = item['barrage'].split('万')[0]
            if playVolumeStr.find("-") > 0:
                salaryArray = playVolumeStr.split('-')
                item['barrage'] = float(salaryArray[0]) * 10000

        params = [item['title'], item['author'], item['playVolume'],
                  item['barrage'], item['overallRatings'], item['rank'], item['link'], item['like_on'],
                  item['coin_on'], item['collect_on'], item['type']]
        jobDao = JobDao()
        result = jobDao.creatJobData(params)
        if result > 0:
            print("保存成功")
        else:
            print("保存失败")
            pass
        return item
