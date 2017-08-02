'''
    获取万方各个类别所有期刊的链接。只需要一开始跑，然后保存在文件里即可
'''
import urllib
import http.cookiejar as cookielib
from html.parser import HTMLParser
import json

class ConnectToClassificationPage():#访问每个类别的网站
    def __init__(self):
        self.hosturl='http://c.wanfangdata.com.cn/PeriodicalSubject.aspx?'
        self.headers={'Upgrade-Insecure-Requests':1,
                      'Connection':'keep-alive',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
                      'Host':'c.wanfangdata.com.cn',
                      'Referer':self.hosturl}
        self.cur_page = ""
        self.cookie = cookielib.CookieJar()
        self.handler=urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler,urllib.request.HTTPHandler)

    def specific_page_connect(self,NodeId,PageNo="1"):#访问特定类的特定页
        postdata=urllib.parse.urlencode({"NodeId":NodeId,"PageNo":PageNo})
        #print(postdata)
        req=urllib.request.Request(self.hosturl+postdata,headers=self.headers)
        result = self.opener.open(req)
        html=result.read().decode("utf-8")
        self.cur_page = html
        return html

    def save_cur_page(self,file_name="./doc/class_page.txt"):
        f = open(file_name, "w")
        f.write(self.cur_page)
        f.close()
        return True

    def set_cur_page(self,html):
        self.cur_page = html
        return True

class ClassPageParser( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_journal = False#基于 <span class="link-wraper col-3"> 判断这个是不是期刊，从而获得其href
        self.is_href = False#基于<a class="link" href='Periodical-ahzyxyxb.aspx'>安徽中医药大学学报判断，这个就是期刊的链接
        self.is_page_num = False
        self.cur_href = ""
        self.journal_href = {}
        self.page_num = "0"

    def handle_starttag(self, tag, attrs):
        if tag=="span":
            try:
                if attrs[0][1] == "link-wraper col-3":
                    self.is_journal = True
                elif attrs[0][1] == "page_link":
                    self.is_page_num = True
            except:
                pass
        if self.is_journal and tag=="a":
            try:
                if attrs[0][1]=="link" and attrs[1][0]=="href":
                    self.is_href=True
                    self.cur_href=attrs[1][1]
                    self.is_journal=False
                else:
                    pass
            except:
                pass

    def handle_data(self, data):
        if self.is_href:
            self.journal_href[data.replace("\n","").replace("\r","").replace(" ","")] = self.cur_href
            self.is_href = False
        if self.is_page_num:
            self.page_num = data.split("/")[1]
            self.is_page_num = False

    def get_journal_href(self):
        return self.journal_href

    def get_page_num(self):
        return self.page_num

def readClassPage( file_path="./doc/class_page.txt" ):
    search_page = open(file_path,"r")
    page=""
    for line in search_page.readlines():
        page+=line
    return page

if __name__ == "__main__":
    class_index = json.load(open("./doc/classification_index.json", "r",encoding="utf-8"))
    for class_name in class_index.keys():
        node_id = class_index[class_name]
        c = ConnectToClassificationPage()
        page = c.specific_page_connect(NodeId=node_id)
        parser = ClassPageParser()
        parser.feed( page )
        page_number = parser.get_page_num()
        journal_href = {}
        for i in range(1,int(page_number)+1):
            page = c.specific_page_connect(NodeId=node_id,PageNo=str(i))
            parser = ClassPageParser()
            parser.feed( page )
            journal_href.update(parser.get_journal_href())
        json.dump(journal_href,open("./doc/"+class_name+".json","w",encoding="utf-8"))
        print("%s is over"%(class_name))
    '''
    c.save_cur_page()
    class_page = readClassPage()
    page = readClassPage()
    '''
