"""
    Function: 
"""
import os
import unittest
import sys
sys.path.append("..")
from src.mexcel import ExcelCase
from src.common import SJ
from src.memail import *
from conf.settings import *
from BeautifulReport import BeautifulReport

def run_without_report():
    """
    运行excel中的测试用例。自动填充结果，但不输出测试报告，也不发送邮件
    :return: None
    """
    result = {}
    suite = unittest.TestLoader().loadTestsFromTestCase(SJ)
    test_result = unittest.TextTestRunner(verbosity=1).run(suite)
    for case, reason in test_result.failures:
        result[case.id()] = 'Fail'
    for case, reason in test_result.errors:
        result[case.id()] = 'Fail'
    # 将失败结果写入Excel中
    ExcelCase().put_result(result)

def run_with_report():
    """
    采用测试报告文件中对unittest库的二次封装，运行excel中的测试用例。自动填充结果，并输出测试报告
    :return: 成功率, 如0.5
    """
    test_suite = unittest.defaultTestLoader.discover(start_dir='../src', pattern='common.py')
    result = BeautifulReport(test_suite)
    result.report(filename=os.path.basename(REPORT_PATH), description=REPORT_DESC, log_path=os.path.dirname(REPORT_PATH))
    # 过滤出失败的结果
    fail_result = {}
    for info in result.result_list:
        if info[4] == '失败':
            fail_result[info[1]] = info[4]
    # 将失败结果写入Excel中
    ExcelCase().put_result(fail_result)
    return (len(result.result_list) - result.failure_count) / len(result.result_list)


def main():
    """
    执行测试用例，根据settins.py的配置，决定是否输出测试报告，是否发送邮件
    :return: None
    """
    if IS_REPORT:
        pass_rate = run_with_report()
        if IS_EMAIL and pass_rate > PASS_RATE:
            send_mail('测试邮件', plain_contant=None, attach=REPORT_PATH)
    else:
        run_without_report()

if __name__ == '__main__':
    main()
    import os
    os.system("pause")
