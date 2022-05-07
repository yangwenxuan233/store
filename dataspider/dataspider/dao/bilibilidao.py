from ..dao.basedao import BaseDao


class JobDao(BaseDao):

    def creatJobData(self, params=None):
        sql = "insert into t_bilibili_data (t_bilibili_title,t_bilibili_author,t_bilibili_playvolume,t_bilibili_barrage," \
              "t_bilibili_overallratings,t_bilibili_rank,t_bilibili_link,t_bilibili_like_on,t_bilibili_coin_on,"\
              "t_bilibili_collect_on,t_bilibili_type) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        result = self.execute(sql, params)
        self.commit()
        return result
        pass

    def statisticplayvolume(self, type):
        sql = "select t_bilibili_playvolume from t_bilibili_data where t_bilibili_type='"+type+"' and t_bilibili_rank<=5"
        self.execute(sql, ret='dict')
        data = self.fetchall()
        return data
        pass

    def statistictype(self):
        sql = "select t_bilibili_type from t_bilibili_data group by t_bilibili_type"
        self.execute(sql, ret='dict')
        data = self.fetchall()
        return data
        pass
