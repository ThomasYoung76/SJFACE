"""
    Function: 
"""
import os

# 接口参数
PROTO = "https"     # 默认协议类型
HOST = "plms.3jyun.com" # 默认域名

# 项目路径
HOME_PATH = os.path.dirname(os.path.dirname(__file__))

# 测试用例路径
CASE_FILE = r"E:\workspace\interface\cases\三江智慧云接口测试用例.xls"

# log
IS_PRINT=False   # 是否记录日志

# 测试报告
IS_REPORT = True    # 是否输出测试报告
REPORT_PATH = r"E:\workspace\interface\result\测试报告.html"    # 测试报告路径
REPORT_DESC = "接口测试"    # 测试报告描述

# 邮件
IS_EMAIL = False    # 是否发送邮件
PASS_RATE = 0.5   # 限制成功率达到多少之后才发送邮件，0则不做限制， 取值[0, 1]
MAIL_HOST = 'smtp.exmail.qq.com'     # 设置邮箱服务器
MAIL_USER = ''  # 用户名
MAIL_PASSWORD = ''             # 密码
SENDER = ''   # 发件人
RECEIVERS= ['']     # 收件人
CC = ['']                   # 抄送人
