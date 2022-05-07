# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .dao.jobdao import JobDao
import re
class DataspiderPipeline:
    def process_item(self, item, spider):
        print(item['job_name'], end="\t")
        print(item['job_company'], end="\t")
        print(item['job_salary'], end="\t")
        print(item['job_address'], end="\t")
        print(item['job_type'],end='\t')
        print(item['job_date'], end="\t")
        print(item['job_info'], end="\n")

        item['job_info'] = re.sub("<[^>]*?>","",item['job_info'])


        # 数据采集  数据处理 数据的存储（数据库） 数据分析（普通和机器学习）和可视化
        # 处理数据
        salary = item['job_salary']
        job_highsalary = 0
        job_lowsalary = 0
        job_meansalary = 0
        job_city = ''

        # 处理城市
        job_address = item['job_address']
        if job_address.find('-'):
            job_city = job_address.split('-')[0]
            pass
        else:
            job_city = job_address
            pass

        if salary.find('万/月') > 0:
            salaryStr = salary.split('万/月')[0]
            if salaryStr.find('-') > 0:
                salaryArray = salaryStr.split('-')
                job_lowsalary = float(salaryArray[0]) * 10000
                job_highsalary = float(salaryArray[1]) * 10000
                job_meansalary = (job_lowsalary + job_highsalary)/2
                pass
            else:
                job_meansalary = job_lowsalary = job_highsalary = float(salaryStr) * 10000
            pass
        pass
        if salary.find('千/月') > 0:
            salaryStr = salary.split('千/月')[0]
            if salaryStr.find('-') > 0:
                salaryArray = salaryStr.split('-')
                job_lowsalary = float(salaryArray[0]) * 1000
                job_highsalary = float(salaryArray[1]) * 1000
                job_meansalary = (job_lowsalary + job_highsalary)/2
                pass
            else:
                job_meansalary = job_lowsalary = job_highsalary = float(salaryStr) * 1000
            pass
        pass
        if salary.find('万/年') > 0:
            salaryStr = salary.split('万/年')[0]
            if salaryStr.find('-') > 0:
                salaryArray = salaryStr.split('-')
                job_lowsalary = float(salaryArray[0]) * 10000 / 12
                job_highsalary = float(salaryArray[1]) * 10000 / 12
                job_meansalary = (job_lowsalary + job_highsalary)/2
                pass
            else:
                job_meansalary = job_lowsalary = job_highsalary = float(salaryStr) * 10000 / 12
            pass
        pass
        if salary.find('元/天') > 0:
            salaryStr = salary.split('元/天')[0]
            if salaryStr.find('-') > 0:
                salaryArray = salaryStr.split('-')
                job_lowsalary = float(salaryArray[0]) * 22
                job_highsalary = float(salaryArray[1]) * 22
                job_meansalary = (job_lowsalary + job_highsalary)/2
                pass
            else:
                job_meansalary = job_lowsalary = job_highsalary = float(salaryStr)
            pass
        pass
        params = [item['job_name'], item['job_company'], item['job_address'], item['job_date'],
                  item['job_salary'], item['job_url'], item['job_type'], job_city, item['job_info'],
                  job_lowsalary, job_highsalary, job_meansalary]

        if job_meansalary > 0:  # 如果没有显示工资，则不存入数据库
            jobDao = JobDao()
            result = jobDao.createJobData(params)
            if result > 0:
                print('保存成功')
                pass
            else:
                print('保存失败')
                pass
            return item