"""
    Function: 处理excel文件，excel扩展名只能为xls，从excel中获取测试用例，并向excel中写入测试结果
"""
import json
import pandas as pd
import numpy as np
import xlwt
import xlrd
import collections
from xlutils.copy import copy
from conf.settings import *

class ExcelCase(object):
    """
        Excel用例中列名为["case_id", "case_name", "api", "method", "header", "params", "body_data", "retcode",
        "check_path", "expect_equal", "expect_true", "result", "comment"]
        对应的中文列名为:["用例编号", "用例标题", "接口名", "请求方法", "消息头", "请求参数"， "消息体", "结果码", "检查路径",
        "期望值", "期望为真", "用例结果", "注释"]
    """
    def __init__(self, case_file=CASE_FILE):
        """
        :param case_file: 用例文件路径
        """
        self.case_file = case_file
        self.titles, self.cases = self.get_cases()

    def get_cases(self):
        """
        从测试用例文件中获取测试用例
        :return:
            (titles, cases)
            titles: 测试用例每列标题组成的列表
            cases: 每条测试用例组成的2维列表
        """
        # 读取excel用例文件，存为DataFrame结构，分别将列名和数据, 转换为ndarray对象后，再转化为列表
        with xlrd.open_workbook(filename=self.case_file, encoding_override='gbk') as content:
            df_case = pd.read_excel(content, engine='xlrd')
        df_attr = df_case.keys()
        cases = np.array(df_case).tolist()
        titles = np.array(df_attr).tolist()
        # 将列表中的no.nan转换成None,并且去除左右两边的\s,\n,\t等空格类型, str(dict)类型转换为dict数据
        titles = list(map(lambda x: x.strip(), titles))
        for index, case in enumerate(cases):
            # json.loads(json.dumps(eval(x)))将eval(x)序列化成json字符串后反序列成原python对象
            cases[index] = list(map(lambda x: json.loads(json.dumps(eval(x))) if str(x).lstrip().find('{') == 0 else x, case))
            cases[index] = list(map(lambda x: x.strip() if isinstance(x, str) else x, case))
            cases[index] = list(map(lambda x: None if pd.isna(x) else x, case))
        return (titles, cases)

    def drop_comment(self):
        """
        去掉注释行
        :return:
        """
        try:
            index_comment = self.titles.index('comment')
        except:
            index_comment = self.titles.index("注释")
        # 过滤掉存在注释符#的注释用例
        self.cases = list(filter(lambda x: not str(x[index_comment]).startswith('#'), self.cases))

        # 用例注释列存在"?"则单独调试该用例
        debug_cases = []
        for case in self.cases:
            if "?" == case[index_comment] or "？" == case[index_comment]:
                debug_cases.append(case)
        if debug_cases:
            self.cases = debug_cases

        # 去掉注释列
        self.titles.pop(index_comment)
        for case in self.cases:
            case.pop(index_comment)


    def handle_cases(self):
        """
        处理excel中获取的测试用例。过滤掉不符合条件的用例，合并补充检查的行
        检查点合并成一个tuple，用列表包含
        :return: 处理完成的测试用例
            [case_id, case_name, api, method, header, params, body_data, retcode,
            [(check_path, expect_equal, expect_true), (check_path2, expect_equal2， expect_true2)...], result]
        """
        # titles, cases = self.get_cases()  # 获取excel中的用例
        self.drop_comment()
        try:
            index_case_id= self.titles.index('case_id')
        except:
            index_case_id = self.titles.index('用例编号')
        try:
            index_check_path = self.titles.index('check_path')
        except:
            index_check_path = self.titles.index("检查路径")
        # # 过滤掉没有case_need全为空且check_point全为空的行
        # cases = filter(lambda x:any(x[index_case_id:index_case_id+4]) and any(x[index_check_path:index_check_path+3]), cases)
        case_flag = 0  # 用例标识位，是一个完整用例，则加1，否则值不变
        for index, case in enumerate(self.cases):
            case_need = case[index_case_id:index_case_id + 4]   # 用例必填项
            check_point = [tuple(case[index_check_path:index_check_path + 3])]  # 用例检查点
            # 用例必填项无值，用例检查点存在值，则认为该用例为前面用例的补充检查部分，取出用例检查点的值加入前面的用例中
            if not any(case_need) and any(check_point[0]):
                self.cases[index-1][index_check_path].append(tuple(case[index_check_path:index_check_path+3]))
            else:
                case_flag += 1
                self.cases[index] = case[0:index_check_path] + [check_point] + case[index_check_path + 3:]
        # 过滤掉case_id为空的行
        self.cases = list(filter(lambda x: x[index_case_id] is not None, self.cases))
        return self.cases

    def put_result(self, fail_result):
        """
        将测试结果result写入cases_file的result列中
        :param fail_result: dict 失败结果{'case_id':'Fail'}
        :return: None
        """
        titles, cases = self.get_cases()  # 获取excel中的用例
        # 获取case_id列和result列的索引位置
        try:
            id_index = titles.index('case_id')
        except:
            id_index = titles.index("用例编号")
        try:
            result_index = titles.index('result')
        except:
            result_index = titles.index("用例结果")
        # 读取excel, formatting_info为True则保留excel的格式
        rexcel = xlrd.open_workbook(self.case_file, encoding_override='gbk', formatting_info=True)
        wexcel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd对象转化为xlwt对象
        table = wexcel.get_sheet(0)  # 获取excel的第0页

        # 设置失败结果的单元格样式
        style_fail = xlwt.XFStyle()
        style_fail.Font = self.set_font()
        style_fail.borders = self.set_border()
        style_fail.pattern = self.set_pattern()
        style_fail.alignment = self.set_alignment()

        # 设置pass结果的单元格样式
        style_pass = xlwt.XFStyle()
        style_pass.Font = self.set_font()
        style_pass.borders = self.set_border()
        style_pass.alignment = self.set_alignment()
        # pattern.pattern_fore_colour = 3
        # style_pass.pattern = pattern    # 成功用例单元格绿色
        # 过滤出失败用例的case_id 如__main__.SJ.test_my_sjy_2_sj_my_devices_0
        fail_ids = fail_result.keys()
        result = []
        for i, case in enumerate(cases):
            result.append([case[id_index], 'Pass'])  # 在result中标记每个用例id的结果均为Pass
            for fail_id in fail_ids:
                if case[id_index] is not None and case[id_index] in fail_id:
                    result[i][1] = 'Fail'  # 如果该用例id在失败的结果，则结果标记为Fail
        for index, value in enumerate(result):
            row = index + 1
            case_id, case_result = value
            # case_id若为None,则该行为空行，不写结果
            if case_id:
                if case_result == 'Fail':
                    table.write(row, result_index, case_result, style_fail)
                else:
                    table.write(row, result_index, case_result, style_pass)
        wexcel.save(self.case_file)  # xlwt对象的保存

    def update_value(self, value, sheet="自定义变量", varname="cookie"):
        # 读取excel, formatting_info为True则保留excel的格式
        rexcel = xlrd.open_workbook(self.case_file, encoding_override='gbk', formatting_info=True)
        wexcel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd对象转化为xlwt对象
        table = wexcel.get_sheet(sheet)  # 获取excel的sheet页
        row = 0
        col = 1
        for var in self.get_var():
            row += 1
            # 找到Excel中对应的变量
            if var == varname:
                break
            else:
                return None
        style = xlwt.XFStyle()
        style.borders = self.set_border()
        style.font = self.set_font()
        style.alignment = self.set_alignment()
        table.write(row, col, value, style)        # 更新Excel中的值
        wexcel.save(self.case_file)

    def _read_var(self):
        """自定义变量页签中只含有两列，第一列是变量，第二列是值，读取出来为字典，变量是字典的key，值是字典的value"""
        with xlrd.open_workbook(filename=self.case_file, encoding_override='gbk') as content:
            try:
                df_var = pd.read_excel(content, engine='xlrd', sheet_name="自定义变量")
            except:
                return {}
        list_var = np.array(df_var).tolist()
        dict_var = collections.OrderedDict(list_var)
        # dict_var = dict(list_var)
        return dict_var

    def get_var(self):
        return self._read_var()

    def _read_header(self):
        with xlrd.open_workbook(filename=self.case_file, encoding_override='gbk') as workbook:
            try:
                content = workbook.sheet_by_name("默认消息头")
            except:
                return None
            header = content.cell_value(0, 1)
        # dict_header = json.loads(json.dumps(eval(header)))
        dict_header = eval(header)
        return dict_header

    def get_header(self):
        return self._read_header()

    def set_font(self):
        # 设置单元格内字体样式
        font = xlwt.Font()
        font.name = '微软雅黑'
        font.colour_index = 0
        font.size = 10
        font.bold = True
        return font

    def set_alignment(self):
        # 单元格对齐方式
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
        alignment.vert = xlwt.Alignment.WRAP_AT_RIGHT
        return alignment

    def set_border(self):
        # 设置单元个下框线样式
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN  # DASHED虚线   NO_LINE没有  THIN实线
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def set_pattern(self):
        # 设置单元格背景颜色， 失败用例单元格背景颜色置为红色
        pattern = xlwt.Pattern()
        pattern.pattern = pattern.SOLID_PATTERN
        # 单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,  the list goes on...
        pattern.pattern_fore_colour = 2
        return pattern

if __name__ == "__main__":
    EC = ExcelCase()
    # EC.init_var()
    # print(host)
    print(EC.get_var())
    print(EC._read_header())
    # cases = EC.get_cases()
    # print(cases)
    # cases = EC.handle_cases()
    # print(cases)
    # EC.update_value("abc")
