# -*- coding: UTF-8 -*-
import url_manager, html_downloader, html_parser, html_outputer
import urllib.request
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
                print(new_data)
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
    startUrl='http://zu.sh.fang.com/'
    urls_num = 1
    output_file = 'fang_info.html'
    spider = SpiderMain()
    spider.doParser(startUrl, urls_num, output_file)

    # response = urllib.request.urlopen(startUrl)
    # if response.getcode() == 200:
    #     text = response.read().decode('gbk', 'ignore').encode('utf-8')
    # print(text)