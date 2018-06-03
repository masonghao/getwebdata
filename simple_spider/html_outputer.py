# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
class HtmlOurputer:
    def __init__(self):
        self.datas = []

    # 收集结果以供下一步处理
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    # 输出结果到文件
    def output_html(self):
        f = open('output.html', 'w', encoding='utf-8')
        f.write('<html>')
        f.write('<body style="background-color:#efefef;">')
        f.write('<table border="1">')
        for data in self.datas:
            f.write('<tr>')
            f.write('<td><a href="%s" title="%s"> %s </a></td>' % (data['baike_url'], data['baike_url'], data['baike_title']))
            f.write('<td> %s </td>' % data['baike_con'])
            f.write('</tr>')
        f.write('</table>')
        f.write('</body>')
        f.write('</html>')
        f.close()