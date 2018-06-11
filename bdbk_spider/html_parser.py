# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib.parse, re
class HtmlParser:
    def __init__(self):
        pass

    # 解析新的百科收集新链接
    def _get_new_urls(self, url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/item/.+'))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    # 解析新的百科标题和总结
    def _get_new_data(self, url, soup):
        res_data = {}
        res_data['baike_url'] = url
        res_data['baike_title'] = soup.find('h1').get_text()
        res_data['baike_con'] = soup.find('div', class_='lemma-summary').get_text()
        return res_data

    # 解析百科返回新的链接和内容
    def parser(self,page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data