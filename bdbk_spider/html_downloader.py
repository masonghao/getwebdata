# -*- coding: UTF-8 -*-
import urllib.request
import zlib
class HtmlDownloader:
    def __init__(self):
        pass

    # 下载页面内容以供解析
    def download(self, url):
        if url is None:
            return
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            text = response.read().decode('utf-8')
            return text
        return None