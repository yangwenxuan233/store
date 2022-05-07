# -*- coding:utf-8 -*-
# log类
# Author: weisen
# time:20211010


import logging.config
import time
import os
import threading


# 获取当前时间
current_time = time.strftime("%Y_%m_%d", time.localtime())
# 创建log目录
path = r'./log'
if not os.path.exists(path):
    os.makedirs(path)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)-15s %(levelname)-1s  %(name)s  %(threadName)-1s ]  %(message)s'
        },
        'simple': {
            'format': '%(asctime)-15s %(levelname)-1s  %(name)s  %(threadName)-1s ]  %(message)s'
        }
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': './log/{}_debug.log'.format(current_time),  # 日志文件
            'maxBytes': 1024*1024*10,  # 日志大小 10M
            'backupCount': 10,
            'encoding': 'utf-8'  # 日志文件的编码
        }
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        }
    }
}


class Logging():
    def __init__(self,getLogger_Name):
        """
        本类主要重写log功能
        :param getLogger_Name: getLogger name
        """
        logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(getLogger_Name)

    def debug(self, message):
        """
        :param message:
        :return:
        """
        self.logger.debug(message)

    def info(self, message):
        """
        :param message:
        :return:
        """
        self.logger.info(message)

    def warn(self, message):
        """
        :param message:
        :return:
        """
        self.logger.warn(message)

    def warning(self, message):
        """
        :param message:
        :return:
        """
        self.logger.warning(message)

    def error(self, message):
        """
        :param message:
        :return:
        """
        self.logger.error(message)

    def critical(self, message):
        """
        :param message:
        :return:
        """
        self.logger.critical(message)