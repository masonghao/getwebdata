# -*- coding: UTF-8 -*-
import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain:
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOurputer()

    def doParser(self, root_url, max_count=10, output_file='output.html'):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('parser %d: %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parser(new_url, html_cont)
                self.urls.add_new_urls(new_urls, max_count)
                self.outputer.collect_data(new_data)
                count += 1
                if count > max_count:
                    print('统计数目到预定值 %d，停止爬取...' % max_count)
                    break
            except:
                print('parser %d: %s failed.' % (count, new_url))
        self.outputer.output_html(output_file)

if __name__ == '__main__':
    startUrl='https://baike.baidu.com/item/%E4%BA%92%E8%81%94%E7%BD%91%E6%8A%80%E6%9C%AF/617749'
    urls_num = 20
    output_file = 'It_info.html'
    spider = SpiderMain()
    spider.doParser(startUrl, urls_num, output_file)