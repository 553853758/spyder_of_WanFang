from html.parser import HTMLParser

class JournalPageParser( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url_list = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            try:
                if attrs[0][1] == "qkcontent_name" and attrs[1][0]=="href":
                    self.url_list.append(attrs[1][1])
            except:
                pass

    def get_url_list(self):
        return self.url_list

def readJournalPage( file_path="./doc/journal_page.txt" ):
    search_page = open(file_path,"r")
    page=""
    for line in search_page.readlines():
        page+=line
    return page

if __name__ == "__main__":
    p = readJournalPage()
    parser = JournalPageParser()
    parser.feed(p)
    print(parser.get_url_list())

    '''
    result:['http://d.wanfangdata.com.cn/Periodical_zwfx201604001.aspx', 'http://d.wanfangdata.com.cn/Periodical_zwfx201604002.aspx'..
    '''