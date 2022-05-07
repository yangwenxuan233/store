import os

# 基础路径相关
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# D:\standard\ST_test_frame

# 日志相关
LOG_PATH = os.path.join(BASE_PATH, 'logs')
LOG_NAME = "standard_test"
LOG_LEVEL = "DEBUG"

# yaml配置相关
YAML_PATH = os.path.join(BASE_PATH, 'case_data')
BOARD_YAML = os.path.join(BASE_PATH, 'case_data', "board.yaml")
GULF_YAML = os.path.join(BASE_PATH, 'case_data', "gulf.yaml")
OASIS_YAML = os.path.join(BASE_PATH, 'case_data', "oasis.yaml")

# 过程数据相关
OASIS_DATA = os.path.join(BASE_PATH, 'output', 'oasis_data')
GULF_DATA = os.path.join(BASE_PATH, 'output', 'gulf_data')
BOARD_DATA = os.path.join(BASE_PATH, 'output', 'on_board_system_data')

# 报告相关
REPORT_NAME = "standard_test_report"
REPORT_PATH = os.path.join(BASE_PATH, 'output')

# 用例相关
STANDARD_CASE_PATH = os.path.join(BASE_PATH, 'standard_case')
GULF_CASE_PATH = os.path.join(BASE_PATH, 'standard_case', 'gulf')
OASIS_CASE_PATH = os.path.join(BASE_PATH, 'standard_case', 'oasis')
BOARD_CASE_PATH = os.path.join(BASE_PATH, 'standard_case', 'on_board_system')
PRODUCTION_CASE_PATH = os.path.join(BASE_PATH, 'standard_case', 'production')

# SROS相关
# SROS_USER = 'admin'
# SROS_PASSWD = 'admin'

# 邮件相关
MAIL_LIST = ['renxing@standard-robots.com']

# 钉钉相关
DINGTAK_SIGN_TOKEN = "SEC84bab94001b90a068449af705f6152515141f70f176d515e52b311b7f7bc2a73"
DINGTAK_ROBOT_URL_TOKEN = "88bcf7fece844d2049be9739d4bab39eb05c113708043b36166442544bc67fc6"
