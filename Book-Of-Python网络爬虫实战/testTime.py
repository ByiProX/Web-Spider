#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'hstking hstking@hotmail.com'


import time
from myLog import MyLog
''' 这里的myLog 是自建的模块，处于该文件的同一目录下'''

class TestTime(object):
	def __init__(self):
		self.log = MyLog()
		self.testTime()
		self.testLocaltime()
		self.testSleep()
		self.testStrftime()

	def testTime(self):
		self.log.info('开始测试time.time()函数')
		print('当前时间戳为：time.time() = %f' %time.time())
		print('这里返回的是一个浮点型的数值，它是从1970纪元后经过的浮点秒数')
		print('\n')

	def testLocaltime(self):
		self.log.info('开始测试time.localtime()函数')
		print('当前本地时间为：time.localtime() = %s' %str(time.localtime()))
		print('这里返回的是一个struct_time结构的元组')
		print('\n')

	def testSleep(self):
		self.log.info('开始测试time.sleep()函数')
		print('这是个计时器：time.sleep(5)')
		print('闭上眼睛数上5秒就可以了')
		time.sleep(5)
		print('\n')

	def testStrftime(self):
		self.log.info('开始测试time.strftime()函数')
		print('这个函数返回的是一个格式化的时间')
		print('time.strftime("%%Y-%%m-%%d %%X",time.localtime()) = %s' %time.strftime("%Y-%m-%d %X",time.localtime()))
		print('\n')


if __name__ == '__main__':
	tt = TestTime()
