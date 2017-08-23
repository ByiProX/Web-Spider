# MailAutoLogin

from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()
browser.maximize_window()
browser.get('http://mail.qq.com/')

# frame = browser.find_element_by_id('login_frame')
# browser.switch_to.frame(frame)
browser.switch_to.frame('login_frame')
# 登录的操作在某一个frame内，所以在进行朝赵元素的时候要先转到相应的frame

browser.find_element_by_id('u').clear()
browser.find_element_by_id('u').send_keys('wangkx0105@qq.com')
browser.find_element_by_id('p').clear()
browser.find_element_by_id('p').send_keys('WKX299792458QQ')
sleep(2)
browser.find_element_by_id('login_button').click()
# browser.find_element_by_id('login_button').submit()
# submit(）相比较于click(),更容易失败。
sleep(4)
browser.find_element_by_id('composebtn').click()
sleep(4)
# frame = browser.find_element_by_id('mainFrame')
browser.switch_to.frame('mainFrame')
sleep(4)

browser.find_element_by_id('toAreaCtrl').send_keys('wangkx0105@outlook.com')
#
#
