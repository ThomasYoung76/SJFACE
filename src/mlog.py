# coding: utf-8
"""
    记录日志
"""

"""
    sLog 记录器，暴露了应用程序代码能直接使用的接口。
    Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。
    Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。
    Formatter 格式化器，指明了最终输出中日志记录的布局。
"""

import sys
import logging
from datetime import datetime
from conf.settings import *
import shutil

__date__ = "2017-08-14"
__author__  = 'yangshifu'

class sLog():
    def __init__(self, log_name):
        log_dir = os.path.join(HOME_PATH, 'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_name = log_name
        self.log_path = os.path.join(log_dir, self.log_name)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        self.get_logger()

    def get_logger(self):
        """
        创建根容器，放入文件hangler，定义日志formatter
        :is_print: 是否打印在控制台
        :return: 已装载好的logger对象
        """
        # 创建根容器
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 创建Handler容器，以及handler的日志级别
        self.file_handle = logging.FileHandler(self.log_path)
        stream_handler = logging.StreamHandler(sys.stdout)
        self.file_handle.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.DEBUG)
        # 定义Formatter,即记录日志的格式
        formatter = logging.Formatter(fmt= '%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        # 设置handler的日志格式为formatter, 将handler放入根容器中
        self.file_handle.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(self.file_handle)
            if IS_PRINT:
                self.logger.addHandler(stream_handler)
        else:
            self.logger.handlers =[]
            self.logger.addHandler(self.file_handle)
            if IS_PRINT:
                self.logger.addHandler(stream_handler)
        return self.logger

    def log_write(self, msg, level='info'):
        """
        写日志
        :param msg: 日志内容。如：get_current_info() + 'Start browser with %s ...' % browser
        :param level: 日志级别，默认INFO
        :return:
        """
        if level.lower() == 'info':
            self.logger.info(msg)
        elif level.lower() == 'debug':
            self.logger.debug(msg)
        elif level.lower() == 'warn' or level.lower() == 'warning':
            self.logger.warn(msg)
        elif level.lower() == 'error':
            self.logger.error(msg)
        elif level.lower() == 'critical':
            self.logger.critical(msg)
        else:
            self.logger.info(msg)


def get_current_info():
    """日志打印文件名、函数名、行号"""
    file_name = os.path.basename(sys._getframe().f_back.f_code.co_filename) + ' '
    func_name = sys._getframe().f_back.f_code.co_name + ' '
    line_no = '[line:' + str(sys._getframe().f_back.f_lineno) + '] '
    return file_name + func_name + line_no

if __name__ == '__main__':
    swrite = sLog('log.txt').log_write
    swrite(get_current_info()+ 'abcdefgs1', 'ERROR')
    swrite(get_current_info()+ 'abcdefgs2', 'info')
    swrite(get_current_info()+ 'abcdefgs3', 'debug')
    twrite = sLog('1.txt').log_write
    twrite('11111111', 'ERROR')
