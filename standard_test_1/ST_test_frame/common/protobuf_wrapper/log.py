import logging

from sros_log import SrosLog

sros_log = SrosLog("protocol_adapter")
sros_log.sendLogToFile()

# FORMAT = ('%(asctime)-3s %(threadName)-3s'
#           ' %(levelname)-3s %(module)-1s:%(lineno)-1s %(message)s')
# logging.basicConfig(format=FORMAT, filename='protocol_adapter.log')
log = logging.getLogger()
# log.setLevel(logging.INFO)
