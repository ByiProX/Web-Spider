# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import urllib
import os

class QiushiwikiPipeline(object):
    def process_item(self, item, spider):
        today = time.strftime('%Y%m%d', time.localtime())
        fileName = today + 'qiubai.txt'
        imgDir = 'IMG'

        # os.makedirs(imgDir, exist_ok=True) # 巧妙方法，代码更简洁
        if os.path.isdir(imgDir):
            pass
        else:
            os.mkdir(imgDir)

        with open(fileName, 'a') as fp:
            fp.write('-'*50 + '\n' + '*'*50 +'\n')
            fp.write('author:\t %s\n' %(item['author']))
            fp.write('content:\t %s\n' %(item['content']))

            try:
                imgUrl =item['img'][0]
            except IndexError:
                pass
            else:
                imgName = os.path.basename(imgUrl)
                fp.write('img:\t %s\n' %(imgName))
                imgPathName = imgDir + os.sep + imgName  # os.path兼容Windows和Mac
                with open(imgPathName, 'wb') as fpi:
                    response = urllib.urlopen(imgUrl)
                    fpi.write(response.read())
            fp.write('fun:%s\t talk:%s\n' %(item['funNum'],item['talkNum']))
            fp.write('-'*50 + '\n' + '*'*50 +'\n')



        return item
