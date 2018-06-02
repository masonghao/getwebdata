import urllib.request, re
from bs4 import BeautifulSoup
from lib.mshlib import getFileContent,putFileContent
# 获取一个网页内容并本地存档
def getHtml(url, fileName):
    htmlCode1 = urllib.request.urlopen(url)
    htmlcodes = htmlCode1.getcode()
    filecode = htmlCode1.read()
    lens = putFileContent(fileName, filecode)
    print('url请求结果 %s 获取写入文件长度为 %s' % (htmlcodes, lens))

# 获取一个网页存入本地
def parserHtml(fileName):
    fileCode = getFileContent(fileName)

    soup = BeautifulSoup(fileCode, 'html.parser')
    h1 = soup.find('h1').get_text()
    links = soup.find_all('a', href=re.compile(r'/item/.+'))
    linksset = set()
    for link in links:
        linksset.add('https://baike.baidu.com/'+link['href'])
        print(link.name, link.get_text(), link['href'])

    print('百科标题：%s' % h1)
    print(linksset)

if __name__ == '__main__':
    url='https://baike.baidu.com/item/html5'
    fileName = 'data/msong.html'
    # getHtml(url, fileName)
    parserHtml(fileName)