"""
    Function: 
"""
import re

def exec_str(str_value, real_value):
    """
    excel中单元格中的字符串支持引用${real_value}和${path_value},
    $real_value$代表响应报文的消息体， $path_value$代表json格式消息体中某路径的值，路径在check_path列的单元格中定义
    解析并替换字符串的变量为path_value的值，将字符串当作命令来执行
    :param str_value: 从excel中获取的包含自定义变量的字符串，如："'13316976950' in ${path_value}"
    :param real_value: excel中字符串中自定义变量的实际值， 如：['13316976950', 'acb', 'ddd']
    :return: 执行字符串中表达式的结果
    用法示例：
        word = "'13316976950' in ${real_value}"
        real_value = ['13316976950', 'acb', 'ddd']
        print(exec_str(word, real_value))
    """

    # 捕获excel中字符串中包含的自定义变量$real_value$替换为path_value
    new_str_value = re.sub(r'\$\{.*?\}', str(real_value), str_value)
    # 执行字符串中包含的表达式
    result = eval(new_str_value)
    return result

# def replace_var(var):
#     """
#     在字典的值或字符串中查找变量${abc}，若存在，则替换成全局变量中abc的值
#     :param var: 字典或字符串。
#     """
#     var_pattern = '\$\{(\w+)\}'
#     # 字典，将字典的值中${cookie}替换成全局变量中cookie的值，没找到则不做处理
#     if isinstance(var, dict):
#         for key in var:
#             list_var = re.findall(var_pattern, var[key])
#             if list_var:
#                 new_value = list_var[0]
#                 if new_value in globals():
#                     var[key] = globals()[new_value]
#         return var
#     # 字符串，将字符串中${real_value}替换成全局变量中real_value的值
#     elif isinstance(var, str):
#         list_var = re.findall(var_pattern, var)
#         if list_var:
#             for varible in list_var:
#                 if varible in globals():
#                     var = var.replace("${%s}"%varible, globals()[varible])
#             return var

if __name__ == "__main__":
    word = "'13316976950' in ${real_value}"
    real_value = ['13316976950', 'acb', 'ddd']
    print(exec_str(word, real_value))
    # dict_var = {'a': '${bbb}', 'b': '${cookie}'}
    # str_var = "hello${bbb} world ${cookie}"
    # print(replace_var(dict_var))
    # print(replace_var(str_var))
    new_word = "len(${real_value}) == 3"
    print(exec_str(new_word, real_value))
    demo_word = "'OK' == '${real_value}'"
    real_value = "OK"
    print(exec_str(demo_word, real_value))