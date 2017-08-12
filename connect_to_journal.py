'''
    根据期刊链接及期刊号进入对应的期刊
'''

import urllib
import http.cookiejar as cookielib
from html.parser import HTMLParser
import time
import json
import random

class ConnectToJournalPage():
    def __init__(self):
        self.hosturl = 'http://c.wanfangdata.com.cn/'
        self.headers={'Upgrade-Insecure-Requests':1,
                      'Connection':'keep-alive',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
                      'Host':'c.wanfangdata.com.cn',
                      'Referer':'http://c.wanfangdata.com.cn/'}
        self.cur_page = ""
        self.cookie = cookielib.CookieJar()
        self.handler=urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler,urllib.request.HTTPHandler)


    def journal_page_connect(self,journal_suffix):#期刊的后缀
        if journal_suffix[0] == "/":
            journal_suffix = journal_suffix[1:len(journal_suffix)]
        postdata = journal_suffix
        req=urllib.request.Request(self.hosturl+postdata,headers=self.headers)
        try:
            result = self.opener.open(req)
            html=result.read().decode("utf-8")
            self.cur_page = html
            return html
        except:
            print("Time out ot connect to journal. Try again")
            time.sleep(random.uniform(10,21))
            try:
                result = self.opener.open(req)
                html=result.read().decode("utf-8")
                self.cur_page = html
                return html
            except:
                print("Time out ot connect to journal. Give up")
                return "None"
                
            

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

if __name__ == "__main__":
    c = ConnectToJournalPage()
    c.journal_page_connect("/periodical/zwfx/2016-4.aspx")
    c.save_cur_page()
    print("over")