import urllib
import http.cookiejar as cookielib

class ConnectToAriclePage():
    def __init__(self):
        self.headers={'Upgrade-Insecure-Requests':1,
                      'Connection':'keep-alive',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
                      'Host':'d.wanfangdata.com.cn'}
        self.cur_page = ""
        self.cookie = cookielib.CookieJar()
        self.handler=urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler,urllib.request.HTTPHandler)

    def article_page_connect( self,url ):
        if 'http' in url:
            try:
                req=urllib.request.Request(url,headers=self.headers)
                result = self.opener.open(req)
                html=result.read().decode("utf-8")
                self.cur_page = html
            except:
                print("Cannot connect to article:%s"%(url))
                return False
        return html

    def save_cur_page(self,file_name="./doc/article_page.txt"):
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
    #url = 'http://d.wanfangdata.com.cn/Periodical_zhpf201706005.aspx'
    #url = 'http://d.wanfangdata.com.cn/Periodical/zwfx201604001'
    url = 'http://d.wanfangdata.com.cn/Periodical/abjbtb201703003'
    c = ConnectToAriclePage()
    html = c.article_page_connect(url)
    c.save_cur_page()
    print("over")