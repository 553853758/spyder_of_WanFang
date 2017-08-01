from html.parser import HTMLParser

class ArticlePageParser( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = {}
        self.in_span = False#因为有的标签在span里，而"pre"在前一个类型里，如：<div class="pre "><span>摘要：</span></div>
        self.is_pre = False
        self.has_pre = False
        self.is_text = False
        self.is_title = False
        self.label = ""
        self.text_label = ""#这个"text"使用哪个tag
        '''
        #下面这个是判断参考文献的方法
        self.cankao_count = 0
        self.yinzheng_count = 0
        self.is_cankao = False
        self.is_yinzheng = False
        self.is_count = False
        '''

    def handle_starttag(self, tag, attrs):
        try:
            if attrs[0][1] == "pre":
                self.is_pre = True
            else:
                pass
        except:
            pass
        if self.has_pre:
            try:
                if attrs[0][1] == "text":
                    self.is_text = True
                    self.text_label = tag
                else:
                    pass
            except:
                pass
        if tag == "span":
            self.in_span = True
        if tag == "meta":
            try:
                if attrs[1][1] == "description":
                    self.data_list["摘要"]=attrs[0][1].replace("\n","。").replace("\r","")
                else:
                    pass
            except:
                pass
        if tag == "title":
            self.is_title = True
        '''
        if tag == "div":
            try:
                if attrs[0][1] == "map-item cite cite1":
                    self.is_cankao = True
                elif attrs[0][1] == "map-item ref ref1":
                    self.is_yinzheng = True
                elif  attrs[0][1] == "count":
                    self.is_count = True
            except:
                pass
        '''

    def handle_data(self, data):
        #print(data)
        if data=="\n":
            return False
        if len(data) == data.count(" ")+data.count("\n")+data.count("\r"):
            return False
        if len(data) == 0:
            return False
        if self.is_title:
            self.data_list["标题"] = data
            self.is_title = False
        if self.is_pre:
            self.label = data.replace("：","").replace(":","")
            self.is_pre = False
            self.has_pre = True
        '''
        if self.is_cankao and self.is_count:
            self.cankao_count = int( data.replace(")","").replace("(","") )
            self.is_cankao = False
            self.is_count = False
        if self.is_yinzheng and self.is_count:
            self.yinzheng_count = int( data.replace(")","").replace("(","") )
            self.is_yinzheng = False
            self.is_count = False
        '''
        if self.has_pre and self.is_text:
            if self.label not in self.data_list:
                #print(self.label)
                #print(self.data_list)
                self.data_list[self.label] = data.replace("\n","").replace("\r","").replace("\r\n","")
            else:
                if type(self.data_list[self.label]) == list:
                    self.data_list[self.label].append(data.replace("\n","").replace("\r",""))
                else:
                    old_data = self.data_list[self.label]
                    self.data_list[self.label] = [old_data,data.replace("\n","").replace("\r","")]

    def handle_endtag(self, tag):
        if self.is_text:
            if self.text_label == "span":
                if tag=="div":
                    self.is_text = False
                    self.has_pre = False
            elif tag == self.text_label:
                self.is_text = False
                self.has_pre = False

    def get_data_list(self):
        return self.data_list

    def get_abstract(self):
        if "摘要" in self.data_list:
            return self.data_list["摘要"]
        else:
            return ""

    def get_title(self):
        if "标题" in self.data_list:
            return self.data_list["标题"]
        else:
            return ""

    def get_keywords(self):
        if "关键词" in self.data_list:
            return self.data_list["关键词"]
        else:
            return ""

    def get_doi(self):
        if "doi" in self.data_list:
            return self.data_list["doi"]
        else:
            return ""

    def get_author(self):
        if "作者" in self.data_list:
            return self.data_list["作者"]
        else:
            return ""

    def get_organization(self):
        if "作者单位" in self.data_list:
            return self.data_list["作者单位"]
        else:
            return ""

    def get_classification(self):
        if "分类号" in self.data_list:
            return self.data_list["分类号"]
        else:
            return ""


def readArticlePage( file_path="./doc/article_page.txt" ):
    search_page = open(file_path,"r")
    page=""
    for line in search_page.readlines():
        page+=line
    return page


if __name__ == "__main__":
    p = readArticlePage()
    parser = ArticlePageParser()
    parser.feed(p)
    print(parser.get_data_list())
    print("over")