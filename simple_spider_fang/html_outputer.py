# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
class HtmlOurputer:
    def __init__(self):
        self.datas = []

    # 收集结果以供下一步处理
    def collect_data(self, data):
        if data is None:
            return
        for x in data:
            self.datas.append(x)

    # 输出结果到文件
    def output_html(self, output_html):
        f = open(output_html, 'w', encoding='utf-8')
        f.write('<html>')
        f.write('<body style="background-color:#efefef;">')
        f.write('<table border="1">')
        for data in self.datas:
            f.write('<tr>')
            f.write('<td><a href="%s" title="%s"> %s </a></td>' % (data['info_url'], data['info_url'], data['info_title']))
            f.write('<td> %s </td>' % data['info_con'])
            f.write('</tr>')
        f.write('</table>')
        f.write('</body>')
        f.write('</html>')
        f.close()