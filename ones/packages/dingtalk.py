#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/9 下午5:42



import requests
import json
from packages.yamlControl import getYamlData
import time
import hmac
import hashlib
import base64
import urllib.parse



class DingTalk:

    def __init__(self):
        """
        钉钉通知API，需要拿到webhook地址和secret，仅仅使用自定义机器人,安全加密方式选择加签
        https://open.dingtalk.com/document/robots/custom-robot-access
        """
        self.getYamlData = getYamlData()['dingTalk']
        self.token = None
        self.secret = None

    def getSecret(self):
        """
        加签算法，参考：https://open.dingtalk.com/document/robots/customize-robot-security-settings
        :return:
        """
        """"""
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp,sign

    def senText(self,msg:str,isAtAll=False):
        """
        发送text内容
        :param msg: 要发送的内容
        :param isAtAll: 是否@所有人
        :return:
        """
        try:
            headers = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
            sendMsg = {
                    "at": {
                        "atMobiles":[],# 被@的手机号
                        "atUserIds":[],# 被@用户userid
                        "isAtAll": isAtAll
                    },
                    "text": {
                        "content":msg
                    },
                    "msgtype":"text"
                }
            timestamp, sign = self.getSecret()
            url =  f'https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={timestamp}&sign={sign}'
            ret = requests.post(url=url, data=json.dumps(sendMsg), headers=headers)
            return ret.text
        except BaseException:
            pass

    def sendLink(self,msg:str,title:str,picUrl='',messageUrl=''):
        """
        发送link类型消息
        :param msg:发送的内容
        :param title:发送的标题
        :param picUrl:图片URL,非必填
        :param messageUrl:点击消息的跳转URL
        :return:
        """
        try:
            headers = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
            sendMsg = {
                    "msgtype": "link",
                    "link": {
                        "text": msg,
                        "title": title,
                        "picUrl": picUrl,
                        "messageUrl": messageUrl
                    }
                }
            timestamp, sign = self.getSecret()
            url = f'https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={timestamp}&sign={sign}'
            ret = requests.post(url=url, data=json.dumps(sendMsg), headers=headers)
            return ret.text
        except BaseException:
            pass

    def sendMarkDown(self,title:str,text:str,isAtAll=False):
        """
        发送markdown信息
        :param title:标题
        :param text: 要发送的内容
        :param isAtAll: 是否@所有人
        :return:
        """
        try:
            headers = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
            sendMsg = {
                         "msgtype": "markdown",
                         "markdown": {
                             "title":title,
                             "text": text
                         },
                          "at": {
                              "atMobiles": [],
                              "atUserIds": [],
                              "isAtAll": isAtAll
                          }
                     }
            timestamp, sign = self.getSecret()
            url = f'https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={timestamp}&sign={sign}'
            ret = requests.post(url=url, data=json.dumps(sendMsg), headers=headers)
            return ret.text
        except BaseException:
            pass

    def sendActionCard(self,title:str,text:str,btnOrientation='0',singleTitle='',singleURL=''):
        """
        发送整体跳转ActionCard类型
        :param title:标题
        :param text:要发送的内容
        :param btnOrientation:0：按钮竖直排列；1：按钮横向排列
        :param singleTitle:单个按钮的标题。
        :param singleURL:点击消息跳转的URL
        :return:
        """
        try:
            headers = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
            sendMsg = {
                        "actionCard": {
                            "title": title,
                            "text": text,
                            "btnOrientation": btnOrientation,
                            "singleTitle" : singleTitle,
                            "singleURL" : singleURL
                        },
                        "msgtype": "actionCard"
                    }
            timestamp, sign = self.getSecret()
            url = f'https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={timestamp}&sign={sign}'
            ret = requests.post(url=url, data=json.dumps(sendMsg), headers=headers)
            return ret.text
        except BaseException:
            pass

    def taskType(self,taskType:str):
        """
        应用类型
        :param taskType:应用类型
        :return:
        """
        try:
            if taskType == 'SROS':
                self.token = self.getYamlData['SROS']['token']
                self.secret = self.getYamlData['SROS']['secret']
            elif taskType == 'SRTOS':
                self.token = self.getYamlData['SRTOS']['token']
                self.secret = self.getYamlData['SRTOS']['secret']
            elif taskType == 'debug':
                self.token = self.getYamlData['debug']['token']
                self.secret = self.getYamlData['debug']['secret']
            else:
                # 默认发送到本体测试组
                self.token = self.getYamlData['other']['token']
                self.secret = self.getYamlData['other']['secret']
        except BaseException:
            pass

    def sendStartTask(self,TaskType,TaskName,assign):
        text = \
            f"### 任务:  {TaskName} \n" \
            f"#### 负责人:  {assign} \n" \
            f"#### 任务已受理，正在执行测试计划中的自动化用例..."
        self.taskType(TaskType)
        self.sendMarkDown(title="测试任务通知", text=text)

    def sendNotification(self,TaskType,TaskName,assign,TOTAL,PASS,PASSRate,FAILED,FAILEDRate,BROKEN,BROKENRate,SKIP,SKIPRate,link):
        text = \
               f"### 任务:  {TaskName} \n" \
               f"#### 负责人:  {assign} \n" \
               f"#### 自动化测试结果如下：\n" \
               f" + 用例总数: {TOTAL}\n" \
               f" + 成功:{PASS},比例:{PASSRate}\n" \
               f" + 失败:{FAILED},比例:{FAILEDRate}\n" \
               f" + 阻塞:{BROKEN},比例:{BROKENRate}\n" \
               f" + 跳过:{SKIP},比例:{SKIPRate}\n" \
               f" > ###### 测试报告 [测试报告链接]({link})\n" # link测试报告链接
        self.taskType(TaskType)
        self.sendMarkDown(title="自动化测试结果通知",text=text)