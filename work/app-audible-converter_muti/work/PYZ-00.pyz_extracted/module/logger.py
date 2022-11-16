# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: module\logger.py
"""
添加日志功能 —— 方便跟踪程序的流程 以及 错误排查

用法：
从本模块导入logger即可
from module.logger import logger

logger.debug('The debug message')
logger.error('The error message')
logger.exception('The exception message')
"""
import logging, os, datetime
log_name = 'Epubor'
LOG_PATH = os.path.expanduser('~')
try:
    TMP_PATH = os.path.join(LOG_PATH, log_name + 'Log')
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)
    if os.path.exists(TMP_PATH):
        LOG_PATH = TMP_PATH
except:
    pass

LOG_FILEPATH = os.path.join(LOG_PATH, log_name + datetime.datetime.now().strftime('%Y.%m') + '.log')
logger = logging.getLogger(log_name)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(os.getcwd(), LOG_FILEPATH))
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-[FILE: %(filename)s]-[FUNC: %(funcName)s]-[LINE: %(lineno)d]-[MSG: %(message)s]')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)