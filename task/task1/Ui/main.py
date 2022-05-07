import os
import sys
import unittest

import HTMLTestRunner_cn

sys.path.append(os.path.dirname(__file__))


def run_case():

    # load testcase
    tests = unittest.defaultTestLoader.discover("Ui", pattern="Test*.py")

    # get results
    runner = HTMLTestRunner_cn.HTMLTestRunner(
        title="UiTest",
        description="the results of testing https://weathershopper.pythonanywhere.com/",
        verbosity=1,
        stream=open("results.html", mode="wb")
    )

    runner.run(tests)


if __name__ == '__main__':
    run_case()
