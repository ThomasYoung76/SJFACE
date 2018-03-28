"""
    Function: 接口测试通用测试用例
"""
import unittest
import requests
import json
from src.mjson import *
from conf.settings import *
from src.mexcel import *
from src.mfunc import *
from parameterized import parameterized
from src.mlog import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__author__ = 'YangShiFu'
__date__ = '2018-02-09'


class SJ(unittest.TestCase):
    """
    从excel中获取测试用例，参数化执行。
    """
    # 获取Excel中的测试用例
    EC = ExcelCase()
    cases = EC.handle_cases()

    @classmethod
    def setUpClass(cls):
        # 获取Excel中定义的全局变量
        cls.init_var()
    # expand_params = get_cases(CASE_FILE)[1]
    # ex_params = filter(lambda x: x[0] is not None, expand_params)   # 过滤掉没有case_id的行
    @parameterized.expand(input=cases)
    def test(self, case_id, case_name, api, method, headers=None, params=None,
             body_data=None, retcode=None, check_point=None, result=None):
        """ """
        # 参数处理
        self.case_id = case_id
        self.case_name = case_name
        self.api = api
        self.method = method.upper()

        # 获取默认消息头中的headers，
        default_header = self.EC.get_header()
        self.headers = self.replace_var(default_header)

        # 处理新的headers，字典中值包含变量时，会从Excel中查找变量
        if headers:
            new_headers = json.loads(json.dumps(eval(headers)))
            new_headers = self.replace_var(new_headers)
        else:
            new_headers = {}
        # 合并headers
        self.headers.update(new_headers)

        # 从Hearders中提取host
        try:
            self.host = self.headers['Host']
        except:
            self.host = HOST

        #  处理params
        if params:
            self.params = json.loads(params)
            self.params = self.replace_var(self.params)
        else:
            self.params = params

        # 处理data
        if body_data:
            self.data = json.loads(body_data)
            self.data = self.replace_var(self.data)
        else:
            self.data = body_data
        # retcode为整数，实际取出来时可能浮点数
        self.retcode = int(retcode) if isinstance(retcode, (int, str, float)) else None

        self.check_point = check_point

        # 日志初始化
        try:
            slog = sLog('log.txt')
            global swrite
            swrite = slog.log_write
        except:
            pass
        swrite("\n\n -------------------- Starting Test %s --------------------\n" % case_id)
        swrite(get_current_info() + "Starting Interface Test. case_id: %s, case_name: %s" % (self.case_id, self.case_name))


        resp = requests.request(self.method, PROTO + "://" + self.host + self.api, data=self.data, headers=self.headers, params=self.params, verify=False)
        resp_body = resp.text   # 响应报文中消息体的文本字符串
        swrite("Request Headers: %s"% self.headers)
        swrite("Request Body: %s" %self.data)
        swrite("Status Code: %s" % resp.status_code)
        swrite("Respond Headers: %s" % resp.headers)
        swrite("Respond Body: %s" % resp_body)

        # 更新Excel中的Cookie值，若存在登录的接口，将会自动更新cookie值
        new_cookie = resp.headers.get('set-cookie')
        if new_cookie:
            excel = ExcelCase()
            excel.update_value(new_cookie, sheet="自定义变量", varname="cookie")

        if self.retcode is not None:
            ret = find_json(resp.json(), '/retCode')
            self.assertEqual(ret, self.retcode)
        if self.check_point:
            for check_path, expect_equal, expect_true in self.check_point:
                if check_path:
                    path_value = find_json(resp.json(), check_path)
                else:
                    # check_path不存在值时，path_value也不存在值
                    path_value = None
                if expect_equal is not None:
                    expect_equal = self.replace_var(expect_equal)
                    self.assertEqual(str(expect_equal), str(path_value))
                else:
                    # 单元格中包含$path_value$则检查路径对应的值，单元格中包含$real_value$，则检查响应报文的消息体的整个文本字符串
                    if 'path_value' in expect_true:
                        ret = exec_str(expect_true, path_value)
                        # 再次执行eval表达式，获取表达式的值
                        try:
                            ret = eval(ret)
                        except:
                            pass
                        self.assertTrue(ret)
                    elif 'real_value' in expect_true:
                        ret = exec_str(expect_true, resp_body)
                        self.assertTrue(ret)
                    else:
                        pass

    @classmethod
    def _read_var(cls):
        """自定义变量页签中只含有两列，第一列是变量，第二列是值，读取出来为字典，变量是字典的key，值是字典的value"""
        with xlrd.open_workbook(filename=CASE_FILE, encoding_override='gbk') as content:
            try:
                df_var = pd.read_excel(content, engine='xlrd', sheet_name="自定义变量")
            except:
                return {}
        list_var = np.array(df_var).tolist()
        dict_var = dict(list_var)
        return dict_var

    @classmethod
    def init_var(cls):
        """ 将测试用例Excel中自定义的变量转换成全局变量"""
        globals().update(cls._read_var())

    def replace_var(self, var):
        """
        在字典的值或字符串中查找变量${abc}，若存在，则替换成全局变量中abc的值
        :param var: 字典或字符串。
        """
        var_pattern = '\$\{(\w+)\}'
        # 字典，将字典的值中${cookie}替换成全局变量中cookie的值，没找到则不做处理
        if isinstance(var, dict):
            for key in var:
                try:
                    list_var = re.findall(var_pattern, var[key])        # var[key]可能不是字符串引发异常，直接跳过处理
                    if list_var:
                        new_value = list_var[0]
                        if new_value in globals():
                            var[key] = globals()[new_value]
                except:
                    pass
            return var
        # 字符串，将字符串中${real_value}替换成全局变量中real_value的值
        elif isinstance(var, str):
            list_var = re.findall(var_pattern, var)
            if list_var:
                for varible in list_var:
                    if varible in globals():
                        var = var.replace("${%s}" % varible, globals()[varible])
                return var
        return var



if __name__ == "__main__":
    # test_suite = unittest.defaultTestLoader.discover('../scripts', pattern='commom.py')
    # result = BeautifulReport(test_suite)
    # result.report(filename='测试报告', description='三江智慧云测试报告', log_path='../result')
    # unittest.main()
    pass
