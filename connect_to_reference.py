import urllib
import http.cookiejar as cookielib

class ConnectToReferencePage():
    def __init__(self,article_url):
        self.id = ""
        self.parse_article_url(article_url)

        self.cankao = 'http://d.wanfangdata.com.cn/CiteRelation/Ref?'
        self.yinzheng = 'http://d.wanfangdata.com.cn/CiteRelation/Cite?'
        self.parameter = {"id":self.id}
        self.headers={'Upgrade-Insecure-Requests':1,
                      'Connection':'keep-alive',
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
                      'Host':'d.wanfangdata.com.cn'}
        self.cur_page = ""
        self.cookie = cookielib.CookieJar()
        self.handler=urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler,urllib.request.HTTPHandler)

    def parse_article_url(self,article_url):
        if "_" in article_url:
            self.id = article_url.split("_")[-1].split(".")[0]
        else:
            self.id = article_url.split("/")[-1]
        return True

    def connect_to_reference(self,ref_type="cankao",page = 1):
        self.parameter["page"] = page
        postdata = urllib.parse.urlencode(self.parameter)
        if ref_type == "cankao":
            req = urllib.request.Request(self.cankao + postdata, headers=self.headers)
        elif ref_type == "yinzheng":
            req = urllib.request.Request(self.yinzheng + postdata, headers=self.headers)
        else:
            print("Wrong reference type!")
            return False
        html = self.opener.open(req).read().decode("utf-8")
        self.cur_page = html
        return html

    def save_cur_page(self,file_name="./doc/reference_page.txt"):
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
    #没有参考文献：url = 'http://d.wanfangdata.com.cn/Periodical_zhpf201706005.aspx'
    url = 'http://d.wanfangdata.com.cn/Periodical_zwfx201604002.aspx'
    #参考路径：http://d.wanfangdata.com.cn/CiteRelation/Cite?id=zwfx201604002
    #参考路径：http://d.wanfangdata.com.cn/CiteRelation/Ref?id=zwfx201604002
    #http://d.wanfangdata.com.cn/CiteRelation/SameRef?id=zwfx201604002
    url = "http://d.wanfangdata.com.cn/Periodical/abjbtb201703003"#有多个参考文献
    c = ConnectToReferencePage(url)
    html = c.connect_to_cankao()
    c.save_cur_page()
    print("over")