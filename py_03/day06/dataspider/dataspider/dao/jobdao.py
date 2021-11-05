from ..dao.basedao import BaseDao

class JobDao(BaseDao):
    def createJobData(self,params=None):
        sql="insert into t_job_data(job_name,job_company,job_address,job_date,"\
            "job_salary,job_url,job_type,job_city,job_info,job_lowsalary,job_highsalary,job_meansalary) values" \
            "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result=self.execute(sql,params)
        self.commit()
        return result
        pass

    def statisticJobTypeCount(self):
        sql = 'select count(job_type) c,job_type from t_job_data group by job_type'
        self.execute(sql,ret='dict')
        data = self.fetchall()
        return data
        pass

    def statisticJobTypeMeanSalary(self):
        sql = 'select avg(job_meansalary) as money,job_type from t_job_data group by job_type'
        self.execute(sql,ret='dict')
        data = self.fetchall()
        return data
        pass

    def statisticJobCitySalary(self):
        sql = 'select avg(job_meansalary) as money,job_city from t_job_data group by job_city order by money desc'
        self.execute(sql, ret='dict')
        data = self.fetchall()
        return data
        pass

    def getAllJobInfo(self):
        sql = 'select * from t_job_data'
        self.execute(sql, ret='dict')
        data = self.fetchall()
        return data
        pass

    pass