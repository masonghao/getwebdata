# -*- coding: UTF-8 -*-
import urllib.request, re
from bs4 import BeautifulSoup

new_urls = set()
old_urls = set()
info_list = []

# 下载页面内容以供解析
def get_html(url):
    if url is None:
        return
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        # text = response.read().decode('utf-8')
        text = response.read()
        return text
    return None

# 解析新的百科收集新链接
def parse_url(url, soup):
    the_urls = set()
    links = soup.find_all('a', href=re.compile(r'http:\/\/jobs\.zhaopin\.com\/.+\.htm'))
    for link in links:
        urls = link['href']
        new_full_url = urllib.parse.urljoin(url, urls)
        the_urls.add(new_full_url)
    return the_urls

# 添加新链接集合到链接池
def add_new_urls(urls):
    if urls is None or len(urls) == 0:
        return
    for url in urls:
        add_new_url(url)

# 添加新链接到链接池
def add_new_url(url):
    if url is None:
        return
    if url not in new_urls and url not in old_urls:
        new_urls.add(url)

# 收集单页所有简历链接地址
def collect_one_page(url):
    con = get_html(url)
    if con:
        soup = BeautifulSoup(con, 'html.parser', from_encoding='utf-8')
        links = parse_url(url,soup)
        link = soup.find('a', class_='next-page')
        next_url = link.get('href')
        return links, next_url

# 获取所有简历地址
def get_all_jl_url(start_url):
    next_url=start_url
    count = 0
    while next_url:
        count += 1
        if count == 39:
            break
        print('geturl %s %s' % (count, next_url))
        links, next_url = collect_one_page(next_url)
        add_new_urls(links)

# 解析一份简历信息
def parse_jl(url):
    info = dict()
    con = get_html(url)
    if con:
        soup = BeautifulSoup(con, 'html.parser', from_encoding='utf-8')
        info['url'] = url
        info['titles'] = soup.find('h1').get_text()
        info['company'] = soup.find('h2').get_text()
        info['zhiwei'] = soup.find('ul', class_='terminal-ul clearfix').get_text()
    return info

# 输出结果到文件
def output_html(output_html):
    datas = info_list
    f = open(output_html, 'w', encoding='utf-8')
    f.write('<html>')
    f.write('<body style="background-color:#efefef;">')
    f.write('<table border="1">')
    for data in datas:
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

# 获取所有简历信息到一个list
def save_all():
    i = 0
    lens = len(new_urls)
    for jl_url in new_urls:
        info = parse_jl(jl_url)
        info_list.append(info)
        i+=1
        print('%s/共 %s 份，解析简历 %s' % (i, lens, jl_url))

# 程序执行入口
def main(start_url, file_name):
    get_all_jl_url(start_url)
    save_all()
    output_html(file_name)
    print('解析完毕！')

if __name__ == '__main__':
    start_url='http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E4%B8%8A%E6%B5%B7&sm=0&isfilter=0&fl=538&isadv=0&sg=5afc8f6be3464df48b08c911bc3ad14f&p=39'
    main(start_url, 'zhiliantest.html')