import urllib.request, re
from bs4 import BeautifulSoup

# url 管理器
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

# html 下载器
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

# html 解析器
class HtmlParser:
    def __init__(self):
        pass

    # 收集列表单页所有简历链接地址
    def parserlist(self, url, html_cont):
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        the_urls = set()
        links = soup.find_all('a', href=re.compile(r'http:\/\/jobs\.zhaopin\.com\/.+\.htm'))
        for link in links:
            urls = link['href']
            new_full_url = urllib.parse.urljoin(url, urls)
            the_urls.add(new_full_url)
        link = soup.find('a', class_='next-page')
        next_url = link.get('href')
        return the_urls, next_url

    # 收集单页所有简历链接地址
    def parserinfo(self, url, html_cont):
        info = dict()
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        info['url'] = url
        info['titles'] = soup.find('h1').get_text()
        info['company'] = soup.find('h2').get_text()
        info['zhiwei'] = soup.find('ul', class_='terminal-ul clearfix').get_text()
        return info

# html 输出
class HtmlOurputer:
    def __init__(self):
        self.datas = []

    # 收集结果以供下一步处理
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    # 输出结果到文件
    def output_html(self, output_html):
        f = open(output_html, 'w', encoding='utf-8')
        f.write('<html>')
        f.write('<body style="background-color:#efefef;">')
        f.write('<table border="1">')
        for data in self.datas:
            f.write('<tr>')
            f.write('<td><a href="%s" title="%s"> %s </a></td>' % (data['url'], data['url'], data['titles']))
            f.write('<td> %s </td>' % data['company'])
            zhiweiinfo = data['zhiwei']
            zhiweiinfo = zhiweiinfo.replace('\n',' ')
            zhiweiinfo = zhiweiinfo.replace('发布日期','<br/>发布日期')
            zhiweiinfo = zhiweiinfo.replace('工作经验','<br/>工作经验')
            zhiweiinfo = zhiweiinfo.replace('不限','<span style="color:red">不限</span>')
            zhiweiinfo = zhiweiinfo.replace('1-3年','<span style="color:red">1-3年</span>')
            zhiweiinfo = zhiweiinfo.replace('1年以下','<span style="color:red">1年以下</span>')
            f.write('<td> %s </td>' % zhiweiinfo)
            f.write('</tr>')
        f.write('</table>')
        f.write('</body>')
        f.write('</html>')
        f.close()

# 智联招聘职位获取程序入口
class ZhiLianMain:
    def __init__(self):
        self.urls_pg = UrlManager()
        self.urls_jl = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.outputer = HtmlOurputer()

    def doParser(self, start_url, output_file):
        self.urls_pg.add_new_url(start_url)
        #收集所有列表页简历链接
        count = 0
        while self.urls_pg.has_new_url():
            count += 1
            new_url = self.urls_pg.get_new_url()
            print('parser %d: %s' % (count, new_url))
            try:
                new_html = self.downloader.download(new_url)
                urls_jianli, next_page = self.parser.parserlist(new_url, new_html)
                self.urls_jl.add_new_urls(urls_jianli)
                self.urls_pg.add_new_urls([next_page])
            except:
                print('geturl %d: %s failed.' % (count, new_url))

        #收集所有简历页职位信息
        count2 = 0
        lens = len(self.urls_jl.new_urls)
        while self.urls_jl.has_new_url():
            new_url = self.urls_jl.get_new_url()
            try:
                new_html = self.downloader.download(new_url)
                info = self.parser.parserinfo(new_url, new_html)
                self.outputer.collect_data(info)

                count2 += 1
                print('parser %d/%d %s' % (count2, lens, new_url))
            except:
                print('parser %d/%d %s failed.' % (count2, lens, new_url))

        #将收集的所有简历页职位信息存入文件
        self.outputer.output_html(output_file)

if __name__ == '__main__':
    start_url='http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E4%B8%8A%E6%B5%B7&sm=0&isfilter=0&fl=538&isadv=0&sg=5afc8f6be3464df48b08c911bc3ad14f&p=39'
    zl = ZhiLianMain()
    zl.doParser(start_url, 'zhiliantest0.html')