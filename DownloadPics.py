from selenium import webdriver
from myLogging import MyLogging
import os
import time
import re

'''
#################################################
# 使用selenium和phantomjs下载火影忍者漫画
#################################################
'''


class DownloadPics(object):

    def __init__(self, url):
        self.url = url
        self.log = MyLogging()
        self.browser = self.get_browser()
        self.save_pics(self.browser)

    def get_browser(self):
        browser = webdriver.PhantomJS()
        try:
            browser.get(self.url)
        except:
            MyLogging.error('open the url %s failed' % self.url)
        browser.implicitly_wait(20)
        return browser

    def save_pics(self, browser):
        pics_title = browser.title.split('_')[0]
        self.create_dir(pics_title)
        os.chdir(pics_title)
        sum_page = self.find_total_page_num(browser)
        i = 1
        while i < sum_page:
            image_name = str(i) + '.png'
            browser.get_screenshot_as_file(image_name)  # 使用PhantomJS避免了截图的不完整，可以与Chrome比较
            self.log.info('saving image %s' % image_name)
            i += 1
            css_selector = "a[href='/comiclist/3/3/%s.htm']" % i  # 该方法感觉还不错呢，不过这个网站确实挺差劲的
            next_page = browser.find_element_by_css_selector(css_selector)
            next_page.click()
            time.sleep(2)
            # browser.implicitly_wait(20)

    def find_total_page_num(self, browser):
        page_element = browser.find_element_by_css_selector("table[cellspacing='1']")
        num = re.search(r'共\d+页', page_element.text).group()[1:-1]
        return int(num)

    def create_dir(self, dir_name):
        if os.path.exists(dir_name):
            self.log.error('create directory %s failed cause a same directory exists' % dir_name)
        else:
            try:
                os.makedirs(dir_name)
            except:
                self.log.error('create directory %s failed' % dir_name)
            else:
                self.log.info('create directory %s success' % dir_name)

if __name__ == '__main__':
    start_url = 'http://comic.kukudm.com/comiclist/3/3/1.htm'
    DL = DownloadPics(start_url)

