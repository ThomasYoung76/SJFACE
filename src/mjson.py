# -*- coding:utf-8 -*-
"""
    Function        :    Http request module
    Author          :    yangshifu
    Create time     :    2018-02-08
"""
import re
import json

def find_json(obj_json, path):
    """
    通过绝对路径（路径格式：'/deviceList[0]/deviceId'）遍历查找json，获取期望的值。
    1.json中key的值不为数组时，遍历方式为'/key1/key2/key3'
    2.json中key2的值为数组时，只能遍历其中一个元素，如遍历key2中第0个元素的方式为'/key1/key2[0]/key3'
    3.支持通配符#：'/deviceList[*]/deviceId'遍历每个/deviceList下的deviceId组成新的列表
    4.path中含有通配符时不再支持json中其他key为数组
    :param obj_json: json值，如resp.json()
    :param path: 查找的绝对路径，不含数组如：'/retCode'，含数组如：'/deviceList[0]/deviceId'，
                支持通配符如：'/deviceList[*]/deviceId'（可获取所有的deviceListId）
    :return: 查找出来的值
    """
    assert path.startswith('/')
    asterisk_flag = False   # 通配符*的标志
    list_path = path.split('/') # 分割路径
    list_path = filter(None, list_path) # 过滤list_path的空值
    for key in list_path:
        # 若key中包含索引，如'deviceList[0]'，拆分成包含tuple的list，即[('deviceList', '0')]
        key_list = re.findall(r'(\w+?)\[(\d+)\]', key)
        key_match = re.findall(r'(\w+?)\[(\*)\]', key)
        # key_list不为空，则key中包含索引
        if key_list:
            # key_list和asterisk_flag均为True的情况不支持
            if asterisk_flag:
                print('Param api include asterisk * and index at the same time, not support.')
                break
            real_key, index = key_list[0]
            obj_json = obj_json.get(real_key)[int(index)]
        # key_match不为空，即key中包含通配符*
        elif key_match:
            asterisk_flag = True
            real_key, asterisk = key_match[0]
            obj_json = obj_json.get(real_key)
        # 若表达式中含通配符*， 则依次处理json数组里的每个元素。不支持含多个*，不支持同时含有*和[\d]
        elif asterisk_flag:
            list_json = []
            for value in obj_json:
                list_json.append(value.get(key))
            obj_json = list_json
        # 若路径中不含通配符*，且key_list和key_match均为空，则key中不含索引，即为json对象的key
        else:
            obj_json = obj_json.get(key)
    return obj_json

def get_json_keys(obj_json, result_key=None):
    """
    获取json对象所有的key，
    :param obj_json:json值
    :param result_key: 列表，默认为None，存放json的key
    :return: result_key
    """
    if not result_key:
        result_key = []
    if not isinstance(obj_json, list):
        obj_json = [obj_json]
    for obj in obj_json:
        for key in obj.keys():
            result_key.append(key)
            value = obj.get(key)
            # value为字典，则继续往下查找key
            if isinstance(value, dict):
                get_json_keys(value, result_key)
            # value为非空列表，且列表中包含的是字典，则继续一层层往下查找key
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    for sub_value in value:
                        get_json_keys(sub_value, result_key)
    return result_key
