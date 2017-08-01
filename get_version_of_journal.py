'''
    一个期刊由多个版本。本代码负责去到期刊的第一页，获得期刊的所有收录，及对应的href
'''
import urllib
import http.cookiejar as cookielib
from html.parser import HTMLParser
import json

class ConnectToVersionPage():#访问每个类别的网站
    def __init__(self):
        self.hosturl='http://c.wanfangdata.com.cn/'
        self.headers={'Upgrade-Insecure-Requests':1,
                      'Connection':'keep-alive',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
                      'Host':'c.wanfangdata.com.cn'}
        self.cur_page = ""
        self.cookie = cookielib.CookieJar()
        self.handler=urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler,urllib.request.HTTPHandler)

    def version_page_connect(self,journal_index):#访问特定类的特定页
        postdata=journal_index
        #print(postdata)
        req=urllib.request.Request(self.hosturl+postdata,headers=self.headers)
        result = self.opener.open(req)
        html=result.read().decode("utf-8")
        self.cur_page = html
        return html

    def save_cur_page(self,file_name="./doc/journal_page.txt"):
        f = open(file_name, "w")
        f.write(self.cur_page)
        f.close()
        return True

    def set_cur_page(self,html):
        self.cur_page = html
        return True

    def close(self):
        self.opener.close()
        self.handler.close()
        return True

class VersionPageParser( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_li = False
        self.in_a = True
        self.is_href = False
        self.is_year=False
        self.cur_year = ""
        self.cur_href = ""
        self.version = {}
        self.has_href = False

    def handle_starttag(self, tag, attrs):
        if tag=="li":
            self.in_li = True
        if self.in_li and tag=="a":
            try:
                if attrs[0][1]=="yearSwitch":
                    self.has_href=True
                    self.is_year=True
                else:
                    pass
            except:
                pass
        if tag=="a":
            try:
                if attrs[1][0]=="href":
                    self.cur_href = attrs[1][1]
                    self.is_href = True
                else:
                    self.is_href = False
            except:
                pass

    def handle_data(self,data):
        #顺序不能错。否则第一个is_year会被保存
        if self.is_href and self.has_href and not self.is_year:
            self.version[self.cur_year][str(data)] = self.cur_href
            self.cur_href = ""
            self.is_href = False
        if self.is_year:
            self.cur_year = data
            if not self.cur_year in self.version:
                self.version[self.cur_year] = {}
            self.is_year = False

    def handle_endtag(self, tag):
        if tag=="li":
            self.in_li = False
            self.has_href = False
            self.is_year = False

    def get_version(self):
        return self.version

def readJournalPage( file_path="./doc/journal_page.txt" ):
    search_page = open(file_path,"r")
    page=""
    for line in search_page.readlines():
        page+=line
    return page

def get_version_of_journal(journal_index):
    c = ConnectToVersionPage()
    html = c.version_page_connect(journal_index)
    parser = VersionPageParser()
    parser.feed( html )
    return parser.get_version()

if __name__ == "__main__":
    zhe_xue = json.load(open("./doc/哲学政法.json", "r",encoding="utf-8"))
    #c = ConnectToVersionPage()
    print( get_version_of_journal(zhe_xue["中外法学"]) )
    '''
    html = c.version_page_connect(zhe_xue["中外法学"])
    c.save_cur_page()
    p = readJournalPage()
    parser = VersionPageParser()
    parser.feed(p)
    print(parser.get_version())
    result:{'2015年': {'4': '/periodical/zwfx/2015-4.aspx',...
    '''