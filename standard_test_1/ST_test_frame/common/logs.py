import logging
import logging.handlers
import os
import time
from ST_test_frame.config import settings


class Logs(object):
    def __init__(self):
        name = settings.LOG_NAME
        self.logger = logging.getLogger(name)

        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}

        log_level = LEVELS.get(settings.LOG_LEVEL, "DEBUG")
        logs_dir = settings.LOG_PATH

        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        log_file_name = f'{name}_{timestamp}.log'
        log_file_path = os.path.join(logs_dir, log_file_name)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=log_file_path,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)

        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(formatter)

        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.NOTSET)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
