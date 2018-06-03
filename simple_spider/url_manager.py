# -*- coding: UTF-8 -*-
class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        self.urls_num = 1
    
    # 添加新链接到链接池
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 添加新链接集合到链接池
    def add_new_urls(self, urls, max_count=None):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            if max_count != None and self.urls_num >= max_count:
                continue
            self.add_new_url(url)
            self.urls_num += 1

    # 检查是否有未爬取的新链接
    def has_new_url(self):
        return len(self.new_urls) != 0

    # 获取下一个要爬取的新链接
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url