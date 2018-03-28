"""
    Function: 
"""
import requests
from conf.settings import *

url = "https://plms.3jyun.com/aaa/login"
login_data = {
            "username": 'weilong.shu@fhsjdz.com',
            "rand": 1517205100434,
            "sign": "69EF420D839B42F1C62E29C93F1FFDE3"
        }

resp = requests.post(url, data=login_data)
print(resp.text)
print(resp.headers)
Cookie = resp.cookies

url = "https://plms.3jyun.com/excel-upload"
file_path = os.path.join(HOME_PATH, 'import') + os.sep + "test_import_3.xlsx"
imp_file = open(file_path, 'rb')
# table = xlrd.open_workbook(file_path)
headers = {
    "Accept":"*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Referer":"https://plms.3jyun.com/index.html",
    "Content-Type":"multipart/form-data; boundary=---------------------------13582806719355",
    "Cookie":"connect.sid=s%3A_08SZ82M6WqTCqgFmanzy14fJVuCGnRF.6mRYL1%2F9yx5LHsDyiuV82feTptPijCLrhNlyMVKyhek; Path=/; Expires=Thu, 15 Mar 2018 05:32:05 GMT; HttpOnly",
}
files ={'file': (file_path, imp_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
# files={"file":imp_file}
print(file_path)
ret = requests.request('POST',url, headers=headers, files=files)
print(ret.status_code)
print(ret.headers)
print(ret.text)
import collections
a = {"a": 1, "c": 2, "d":0, "e": 4}
o_a = collections.OrderedDict(a)
print(o_a)
print(a.items())
hehe = sorted(a.items(), key=lambda x: x[0], reverse=False)
print(hehe)