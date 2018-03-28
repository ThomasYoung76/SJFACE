# Interface
---
基于python + requests + unittest的接口自动化框架，适用于http/https接口测试。

# 框架介绍
---

### 该框架可以做些什么

这个框架借助Excel（Excel扩展名必须为xls）,通过在Excel中填写接口测试相关数据，即可实现接口自动化测试，
测试用例参照cases目录中的模板，通过使用python3的解释器执行scripts/run_main.py文件，
读取Excel测试用例中的每条用例并执行，并将执行结果回写到Excel的测试用例中的result栏中，同时可以生成html格式的可视化的测试报告，
并同时可以通过邮件将该测试报告发送出去。

### 目录结构介绍

interface

	* cases:				// 用于存放测试用例
		三江智慧云接口测试用例.xls			//最新测试用例模板，建议严格参照该格式写测试用例
		三江智慧云接口测试用例_V0.xls		//V0版本测试用例模板，框架初始设计时，采用的测试用例，可忽略
	
	* export:				// 用于存放导出文件，暂未适用
	
	* conf:
		settins.py			// 配置文件，可配置接口的host地址，及协议，路径
	
	* result:				// 用于存放测试报告
		测试报告.html	// 执行用例后，生成的测试报告文件
		
	* scripts：			// 存放接口测试的脚本文件
		demo.py			// 多余文件，可忽略
		plms_login.py	// 多余文件，可忽略，python + requests测试的遗留文件
		run_main.py		// main文件。运行该文件生成测试报告
		
	* src：				// 框架自身接口目录均在这里
		common.py		// 通用的测试脚本文件。该文件利用unittest执行excel中获取的测试用例
		common_V0.py	// V0版本通用的测试脚本文件，可忽略
		memail.py		// 发送邮件的方法
		mexcel.py		// 操作excel的方法
		mexcel_V0.py	// V0版本操作excel的方法，可忽略
		mjson.py		// 用于检查返回的json报文调用的
		mlog.py			// 日志
	
注：运行run_main.py即可执行Excel中测试用例，但需要先把Excel测试用例关闭，否则由于文件被打开无法填写测试结果，导致执行失败。
	
### 部分 API简介

	* run_main.main
		def main():
	    """
	    执行测试用例，根据settins.py的配置，决定是否输出测试报告，是否发送邮件
	    :return: None
	    """

	* mexcel.ExcelCase
		def get_cases(self):
		"""
		从测试用例文件中获取测试用例
		:return:
			(titles, cases)
			titles: 测试用例每列标题组成的列表
			cases: 每条测试用例组成的2维列表
		"""
	
		def handle_cases(self):
		"""
		处理excel中获取的测试用例。过滤掉不符合条件的用例，合并补充检查的行
		检查点合并成一个tuple，用列表包含
		:return: 处理完成的测试用例
			[case_id, case_name, path, method, headers, params, body_data, retcode,
			[(check_path, expect_equal, expect_true), (check_path2, expect_equal2， expect_true2)...], result]
		"""
			
		def put_result(self, fail_result):
		"""
		将测试结果result写入cases_file的result列中
		:param fail_result: dict 失败结果{'case_id':'Fail'}
		:return: None
		"""

	* mjson.find_json
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

	* common.SJ
		class SJ(unittest.TestCase):
	    """
	    从excel中获取测试用例，参数化执行。
	    """
	
	* memail.send_mail	
		def send_mail(subject, plain_contant=None, html_contant=None, attach=''):
			"""
			发送邮件(使用SSL协议发送，腾讯企业邮箱)
			发送邮件，可含附件  -- 修改于2018年2月9日 yangshifu，
			:param subject: 主题
			:param plain_contan: 纯文本内容
			:param plain_contant: 纯html内容
			:param attach:  附件地址，为空则不传附件
			:return:
			"""

	* BeautifulReport
		用于生成测试报告	
	
# 版本变更说明
---

### 初始版本
	完成于2018/2/7。
	V0版本为初始版本，目前已不采用，但仍保留3个后缀为V0的核心文件，该版本具备基本功能，后续版本在此基础上进行扩展。
	功能说明：
		从Excel读取的每行当作一条测试用例来执行，将执行结果写入Excel中。

### 当前版本
	
	当前版本基于基础版本扩展，后续所有功能均在此版本基础上作变更
	
	2018/2/9功能变更说明：
		1. Excel中的测试用例支持多行书写，附加的行仅用于检查json报文。
		2. 新增输出可视化的测试报告，该测试报告包含图表，可在settings.py文件中配置是否输出该测试报告，及其他相关信息
		3. 新增自动发送邮件功能，可将测试报告作为附件发送邮件，可在settings.py中是否发送邮件，及测试通过率达到多少比率时发送，及其他邮件相关信息
	
	2018/2/10功能变更说明：
		1. Excel中新增comment列，用于注释行，被注释的行将不会被执行。
		2. Excel中expect_true列支持两个自定义变量$real_value$和$path_value$。分别代表响应报文消息体的实际值和响应的json报文中某路径（该路径由check_path列定义）对应的实际值。

	2018/3/5：
		1. 优化日志封装模块，增加输出日志，日志中可以查看每个接口的请求报文和响应报文

	2018/3/6：
		1. 增加定义Cookie变量，并在Excel中使用

	2018/3/9：
		1. Excel中新增页签，命名为：“自定义变量”，在这里可以自定义变量，可以在请求消息头（header，param，body_data列）的字典的值中引用变量，引用方式为${var}, 其中var的值在自定义变量页中定义。
	
	2018/3/19：
		1. 优化：原来Excel中单元格headers、body_data等填充json数据，现优化为填充python的字典数据类型。(json数据格式要求比字典严格）	

	2018/3/21：
		1. 修复bug，bug：多条用例含有2个检查点时，后面用例的第二条检查点会加到前面的用例中去；
		2. 自动设置cookie值，测试用例中存在对登录的接口的测试，该接口返回了Cookie值时，每次执行接口测试，均会在excel中自动更新cookie值。 当cookie失效后，第一遍执行会大部分用例失败，重复执行测试用例，可以使用最新的cookie；
		3. 对expect_true单元格的检查支持使用python部分内置函数，如"len(${path_value}) == 4"；
	
	2018/3/22：
		1. Excel中新增页签，命名为:“默认消息头”，定义默认的消息头，避免在Excel用例中重复写消息头中的字段
	
	2018/3/27:
		1. comment列支持“？”值，选定该用例执行
		

	