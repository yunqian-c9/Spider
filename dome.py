import re
from urllib import request

class Spider():
    url = "https://www.huya.com/g/lol"
    root_pattern = '<li class="game-live-item" gid="1">([\s\S]*?)</li>'
    name_pattern = '<i class="nick" title="[\s\S]*?">([\s\S]*?)</i>'
    number_pattern = '<i class="js-num">([\s\S]*?)</i>'

    #获取html文本方法
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        #byts
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    #分析html
    def __analysis(self,htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number':number}
            anchors.append(anchor) #遍历拼合完数据后添加进列表里
        return anchors

    #数据精炼（strip方法去除name前后换行符、空格；把列表转换为str）
    def __refine(self, anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0]
        }

        return map(l, anchors)

    #业务处理（排序）
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True) #内置排序方法
        return anchors

    #给sorted提供key的参数
    def __sort_seed(self, anchor):
        r = re.findall('\d*\.\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number


    """
    显示排序后的数据
    """
    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank ' + str(rank + 1)
                  + ' : ' + anchors[rank]['name']
                  + '    ' + anchors[rank]['number']
                  )

    #入口方法
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)

spider = Spider()
spider.go()