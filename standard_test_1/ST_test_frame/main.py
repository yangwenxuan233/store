import unittest
import HTMLReport
import os
import time
import pathlib
import sys
sys.path.append("../")
from ST_test_frame.common.logs import Logs
from ST_test_frame.config import settings


class RunAllCase(object):
    def __init__(self, file_path_name=''):
        self.init_path = pathlib.Path(settings.STANDARD_CASE_PATH)
        self.logger = Logs()
        if file_path_name:
            self.case_path = list(self.init_path.glob(f"**/{file_path_name}"))[0]
            self.logger.info(f'now run: {self.case_path}')
        else:
            self.case_path = os.path.join(settings.STANDARD_CASE_PATH, file_path_name)
            self.logger.info(f'now run: {self.case_path}')
        self.logger.logger.handlers.pop()

    def all_case(self):
        discover = unittest.defaultTestLoader.discover(self.case_path, pattern="test*.py", top_level_dir=None)
        return discover

    @staticmethod
    def now_time():
        return time.strftime("%Y_%m_%d %H_%M_%S")


def run(file_names):
    c = RunAllCase(file_names)
    cases = c.all_case()
    now = c.now_time()
    runner = HTMLReport.TestRunner(report_file_name=f"{settings.REPORT_NAME}_{now}",
                                   output_path=settings.REPORT_PATH,
                                   description='自动化测试详细的报告')
    runner.run(cases)
    c.logger.info('测试结束，生成基于HTML的测试报告')


if __name__ == '__main__':
    # pass
    file_name = ""
    run(file_name)
