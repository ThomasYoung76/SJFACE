"""
    Function: 
"""
import requests
import sys
sys.path.append("..")
from conf.settings import *
from src.mjson import *
from BeautifulReport import BeautifulReport
import unittest

class TestPLMS(unittest.TestCase):
    # str_headers = """
    # Accept: application/json, text/javascript, */*; q=0.01
    # Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
    # Accept-Encoding: gzip, deflate, br
    # Content-Type: application/json; charset=utf-8
    # DeviceId: weilong.shu@fhsjdz.com
    # Timestamp: 1516694521545
    # Signature: 88dc9c1649cf7d04577f43cedde1e78f
    # X-Requested-With: XMLHttpRequest
    # Referer: https://plms.3jyun.com/index.html
    # """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json; charset=utf-8",
        "DeviceId": "weilong.shu@fhsjdz.com",
        "Timestamp": "1516861101509",
        "Signature": "8ee97d04090defdf1d17409a39f53bfd",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://plms.3jyun.com/index.html",
    }
    @classmethod
    def setUpClass(cls):
        path = '/aaa/login'
        login_url = PROTO + '://' + HOST + path
        login_data = {
            "username": USERNAME,
            "rand": 1517205100434,
            "sign": "69EF420D839B42F1C62E29C93F1FFDE3"
        }
        resp = requests.post(login_url, data=login_data, verify=False)
        cls.cookies = resp.cookies
        print(resp.content)
        # cls.assertEqual(resp.status_code, 200)

    # def a_test_login(self):
    #     api = '/aaa/login'
    #     login_url = proto + '://' + host + api
    #     login_data = {
    #         "username": username,
    #         "rand": 1517205100434,
    #         "sign": "69EF420D839B42F1C62E29C93F1FFDE3"
    #     }
    #     resp = requests.post(login_url, data=login_data)
    #     cookies = resp.cookies
    #     self.assertEqual(resp.status_code, 200)


    def test_add_device(self):
        path = '/api/device'
        self.headers['Timestamp'] = '1516679269330'
        self.headers['Signature'] = 'ee3f809b3289c902f80f5e8d0484d25c'
        # cookies = {"Cookie":"connect.sid=s%3Aps2MZe6TEXiYb_hKiLdpwHFz7yCQKlC6.Y0BmmGsifv3JamIcEJ%2BICsHUFRXvq%2FdaZn2FzGMiak8"}
        data = {"_id":"d5ee11b3e9825443","deviceType_id":"RaspberryPi-3B","deviceName":"123456","deviceDesc":"接口测试","deviceSecret":"66522e2cac051b34185955ee99f7637c","extension":{}}
        resp = requests.post("https" + '://' + HOST + path, data=data, cookies=self.cookies, headers=self.headers)
        print(resp.content)
        self.assertEqual(resp.status_code, 200)

    def test_get_device(self):
        """ 获取设备"""
        path = '/api/device/?filter%5BdeviceType_id%5D=CRT&page=1&rows=10'
        resp = requests.get(proto + '://' + host + path, cookies=self.cookies, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        print(resp.text)


if __name__ == '__main__':
    # test_suite = unittest.defaultTestLoader.discover('../testcase', pattern='test*.py')
    # result = BeautifulReport(test_suite)
    # result.report(filename='测试报告', description='测试deafult报告', log_path='../result')
    unittest.main()
    # a = TestPLMS()
