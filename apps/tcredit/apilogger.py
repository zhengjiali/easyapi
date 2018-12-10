__author__ = 'zhengjiali'
__filename__ = 'apilogger.py'
__date__ = '2018/12/10 下午4:35'

import logging
import datetime

def apiLogger(filename='./logs/tcredit.log'):
    logger = logging.getLogger(__name__)
    t = datetime.datetime.now()-datetime.timedelta(hours=12)
    formatter = logging.Formatter(str(t)+'  %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(level=logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(filename)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger