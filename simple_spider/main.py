# -*- coding: UTF-8 -*-
import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain:
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOurputer()

    def doParser(self, root_url, max_count=10):
        count = 1
        max_count = max_count-1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('parser %d: %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parser(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if count > max_count:
                    break
                count = count + 1
            except:
                print('parser %d: %s failed.' % (count, new_url))
            self.outputer.output_html()

if __name__ == '__main__':
    startUrl='https://baike.baidu.com/item/html5'
    spider = SpiderMain()
    spider.doParser(startUrl, 20)