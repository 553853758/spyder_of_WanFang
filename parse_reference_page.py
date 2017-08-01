from html.parser import HTMLParser

class ReferencePageParser( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reference = []
        self.cur_data = ""
        self.is_reference = ""
        self.div_count = 0
        #下面的用来找下一页
        self.has_many_pages = False
        self.cur_href_page = 0
        self.next_page = False

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            try:
                if attrs[0][1] == "item":
                    self.is_reference = True
                else:
                    pass
            except:
                pass
            if self.is_reference:
                self.div_count+=1
        if tag == "p":
            try:
                if attrs[0][1] == "pager":
                    self.has_many_pages = True
                else:
                    pass
            except:
                pass
        if self.has_many_pages and tag=="a":
            try:
                if attrs[1][0] == "href":
                    try:
                        self.cur_href_page = int(attrs[1][1].split("page=")[1][0:2])
                    except:
                        self.cur_href_page = int(attrs[1][1].split("page=")[1][0])
                    #<a class="page" href="/CiteRelation/Ref?page=22&amp;id=abjbtb201703003">下一页>></a>
                else:
                    pass
            except:
                pass

    def handle_data(self, data):
        if self.is_reference:
            self.cur_data += data.replace("\n","").replace("\r","")#.replace("  ","")
        if "下一页" in data:
            self.next_page = self.cur_href_page

    def handle_endtag(self, tag):
        if self.is_reference and tag == "div":
            self.div_count -= 1
            if self.div_count==0:
                self.reference.append(self.cur_data)
                self.cur_data = ""
                self.is_reference = False

def readReferencePage( file_path="./doc/reference_page.txt" ):
    search_page = open(file_path,"r")
    page=""
    for line in search_page.readlines():
        page+=line
    return page

if __name__ == "__main__":
    p = readReferencePage()
    parser = ReferencePageParser()
    parser.feed(p)
    print( parser.next_page )
    print( parser.reference )
