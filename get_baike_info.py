import urllib.request
from bs4 import BeautifulSoup

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
    links = soup.find_all('a')
    for a in links:
        print(a.name, a['href'], a.get_text())

# 获取本地文件的内容到字符串
def getFileContent(fileName, mods = 'rb'):
    file = open(fileName, mods)
    fileCode = file.read()
    file.close()
    return fileCode

# 输出字符串到一个本地文件
def putFileContent(fileName, filecode, mods = 'wb'):
    f = open(fileName, mods)
    lens = f.write(filecode)
    f.close()
    return lens

if __name__ == '__main__':
    url='http://localhost:8000/article/'
    fileName = 'data/msong.html'
    getHtml(url, fileName)
    parserHtml(fileName)