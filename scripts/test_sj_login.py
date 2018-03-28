"""
    Function: 
"""
import requests
from conf.settings import  *
from src.mfunc import *
import unittest
from BeautifulReport import BeautifulReport

class SJTest(unittest.TestCase):

    def test_login(self):
        """登录我的三江云"""
        path = '/aaa/login'
        login_url = host + path
        data = {"deviceId":"13480879200","rand":1517448528991,"sign":"891323BE40C249E6022A35F6BF940131"}
        resp = requests.post(login_url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['retCode'], 0)
        print(resp.json())
        self.assertEqual(find_json(resp.json(), '/profile/contact/id'), '13480879200')

    def test_device_status(self):
        """ 查询设备状态"""
        path = "/aaa/devStatus"
        data = {
            "ids": "13316976950,0edc7434fc082059f4584ff,076a4335283d3f8879046f2,sjyun_jb_qbl_6001_002,sjyun_jb_qbl_6001_003,4334371fbe90ea4fd9db583,59317dbcc02f1c65,c98fc3c0be0a4710,d06df7facc28d15f"}
        headers = {
            "DeviceId": "13480879200_1500288608201",
            "Timestamp": "1517448530532",
            "Signature": "1e0393b7ee8e67713714410ecf4962ec",
            "Referer": "https://i.3jyun.com/index.html",
        }
        resp = requests.post(host+path, data=data, headers=headers)
        self.assertEqual(resp.json()['retCode'], 0)
        self.assertEqual(find_json(resp.json(), '/devices/13316976950/deviceId'), '13316976950')
        print(resp.json())


    def test_get_device_list(self):
        """ 获取我的设备列表 """
        path = "/aaa/mydevices/13480879200_1500288608201"
        params = {"version": "1517377905080"}
        headers = {
            "DeviceId": "13480879200_1500288608201",
            "Timestamp": "1517448530439",
            "Signature": "d148403ea36b3ed3140dcb070eaf881e",
            "Referer": "https://i.3jyun.com/index.html",
            "Origin": "https://i.3jyun.com"
        }
        resp = requests.get(host+path, params=params, headers=headers)
        devices = find_json(resp.json(), '/deviceList[*]/deviceId')
        self.assertEqual('13316976950' in devices, True)
        print(resp.json())

    def test_add_own(self):
        """关注设备17842819856dee97"""
        path = "/aaa/own/13480879200_1500288608201/17842819856dee97"
        headers = {
            "DeviceId": "13480879200_1500288608201",
            "Timestamp": "1517898984724",
            "Signature": "b483aee54bd5bc0183d63c5849f804c4",
            "Referer": "https://i.3jyun.com/index.html",
            "Origin": "https://i.3jyun.com"
        }
        data = {}
        resp = requests.post(host + path, data=data, headers=headers)
        ret = find_json(resp.json(), '/retCode')
        msg = find_json(resp.json(), '/message')
        self.assertEqual(ret, 0)
        self.assertEqual(msg, 'OK')
        print(resp.json())

    # @unittest.skip('暂不删除')
    def test_del_own(self):
        """ 删除设备17842819856dee97"""
        path = "/aaa/own/13480879200_1500288608201/17842819856dee97"
        data = {}
        headers = {
            "DeviceId": "13480879200_1500288608201",
            "Timestamp": "1517898984724",
            "Signature": "b483aee54bd5bc0183d63c5849f804c4",
            "Referer": "https://i.3jyun.com/index.html",
            "Origin": "https://i.3jyun.com"
        }
        resp = requests.delete(host + path, data=data, headers=headers)
        ret = find_json(resp.json(), '/retCode')
        self.assertEqual(ret, 0)
        print(resp.json())



if __name__ == '__main__':
    # test_suite = unittest.defaultTestLoader.discover('../scripts', pattern='test*.py')
    # result = BeautifulReport(test_suite)
    # result.report(filename='测试报告', description='三江智慧云测试报告', log_path='../result')
    unittest.main()