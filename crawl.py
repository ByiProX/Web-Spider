import requests
import pdfkit
import os
import re
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class Crawler(object):
    """docstring for Crawler."""

    def __init__(self, name, crawl_url):
        self.name = name
        self.crawl_url = crawl_url
        self.domain = '{url.scheme}://{url.netloc}'.format(url=urlparse(self.crawl_url))

    @staticmethod
    def request(url, **kwargs):
        response = requests.get(url, **kwargs)
        return response

    def parse_menu(self, response):
        pass

    def parse_body(self, response):
        pass

    def run(self):
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,

        }

        htmls = []
        for index, url in enumerate(self.parse_menu(self.request(self.crawl_url))):
            html = self.parse_body(self.request(url))
            file_name = '.'.join([str(index), 'html'])
            with open(file_name, 'wb') as f:
                f.write(html)
            htmls.append(file_name)

        pdfkit.from_file(htmls, self.name + '.pdf', options=options)
        for html in htmls:
            os.remove(html)


class WebPageCrawler(Crawler):
    def parse_menu(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        menu_tag = soup.find_all(class_='uk-nav uk-nav-side')[1]
        for li in menu_tag.find_all('li'):
            url = li.a.get('href')
            if not url.startswith('http'):
                url = '.'.join([self.domain, url])
            yield url

    def parse_body(self, response):
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(class_='x-wiki-content')[0]

            title = soup.find('h4').get_text()
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag = soup.new_tag('center')
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)
            html = str(body)

            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith('http'):
                    url = ''.join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return url
                else:
                    return ''.join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html_template = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                            </head>
                            <body>
                            {content}
                            </body>
                            </html>
                            
                            """
            html = html_template.format(content=html).encode('utf-8')
            return html
        except Exception as e:
            logging.error('解析错误', exc_info=True)


if __name__ == '__main__':
    start_url = "http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
    crawler = WebPageCrawler("廖雪峰Git", start_url)
    crawler.run()
