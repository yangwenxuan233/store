#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# @Author: weisen
# @Time: 2022/4/13 下午2:29
# @File: run.py


from main import TaskManager
from packages.logControl import Logging
import sys


class RunService:

    def __init__(self):
        self.logger = Logging('RunService')
        self.taskManager = TaskManager()

    def run(self):
        try:
            self.taskManager.queryTaskStatus()
        except BaseException as e:
            self.logger.error(f'run:{e}')

    def stopService(self):
        try:
            self.taskManager.stopQueryTaskStatus()
        except BaseException as e:
            self.logger.error(f'stopService:{e}')


if __name__ == '__main__':
    Task = RunService()
    Task.run()
    sys.exit(Task.stopService())