import json
import os
import get_version_of_journal
import connect_to_journal
import connect_to_article
import connect_to_reference
import parse_journal_page
import parse_article_page
import parse_reference_page

def get_reference( article_url ):
    connectToReferencePage = connect_to_reference.ConnectToReferencePage(article_url)
    reference_type = ["cankao","yinzheng"]
    reference = {"cankao":[],"yinzheng":[]}
    for ref_type in reference_type:#[0:1]:
        try:
            refer_page = 1
            refer_html = connectToReferencePage.connect_to_reference(ref_type=ref_type,page=refer_page)
            print(refer_page)
            if not refer_html:
                continue
            while True:
                referencePageParser = parse_reference_page.ReferencePageParser()
                referencePageParser.feed(refer_html)
                if len(referencePageParser.reference)>0:
                    reference[ref_type].extend(referencePageParser.reference)
                if not referencePageParser.next_page:
                    break
                else:
                    refer_page = referencePageParser.next_page
                    #print(refer_page)
                    refer_html = connectToReferencePage.connect_to_reference(ref_type=ref_type,page=refer_page)
        except:
            print("Faile to connect to refer:%s"%(ref_type))
            continue
    return reference

if __name__=="__main__":
    journal_type = "哲学政法"
    zhe_xue = json.load(open("./doc/%s.json"%(journal_type), "r",encoding="utf-8"))
    journal_type_path = "./doc/spyder_result/%s" % (journal_type)
    if not os.path.isdir(journal_type_path):
        os.mkdir( journal_type_path )
    journal_name = "中外法学"
    journal_path = (journal_type_path+"/%s") % (journal_name)
    version_of_journal = get_version_of_journal.get_version_of_journal(zhe_xue[journal_name])
    if not os.path.isdir( journal_path ):
        os.mkdir( journal_path )
    for year in list(version_of_journal.keys())[0:1]:
        journal_year_path = (journal_path+"/%s") % (year)
        if not os.path.isdir(journal_year_path):
            os.mkdir(journal_year_path)
        for month in list(version_of_journal[year].keys())[0:1]:
            journal_month_path = (journal_year_path+"/%s") % (month)
            if not os.path.isdir(journal_month_path):
                os.mkdir( journal_month_path )
            #访问这个期刊版本的页面。获得所有文章
            suffix = version_of_journal[year][month]
            connectToJournalPage = connect_to_journal.ConnectToJournalPage()
            journal_html = connectToJournalPage.journal_page_connect(suffix)
            connectToJournalPage.close()
            journalPageParser = parse_journal_page.JournalPageParser()
            journalPageParser.feed(journal_html)
            article_url_list = journalPageParser.get_url_list()
            main_result = open(journal_month_path+"/检索结果.txt","w")
            main_result.write("标题\t")
            main_result.write("关键词\t")
            main_result.write("摘要\t")
            main_result.write("作者\t")
            main_result.write("单位\t")
            main_result.write("DOI\t")
            main_result.write("分类号\n")
            for article_url in article_url_list:#[0:1]:
            #for article_url in ["http://d.wanfangdata.com.cn/Periodical/abjbtb201703003"]:
                print(article_url)
                connectToArticlePage = connect_to_article.ConnectToAriclePage()
                article_html = connectToArticlePage.article_page_connect(article_url)
                connectToArticlePage.close()
                articlePageParser = parse_article_page.ArticlePageParser()
                articlePageParser.feed(article_html)
                data_list = articlePageParser.get_data_list()
                #print(data_list)
                abstract = articlePageParser.get_abstract()
                keywords = articlePageParser.get_keywords()
                title = articlePageParser.get_title()
                doi = articlePageParser.get_doi()
                author = articlePageParser.get_author()
                organization = articlePageParser.get_organization()
                classification = articlePageParser.get_classification()
                error_place = "Write file"
                if len(abstract) == 0:
                    abstract = "none"
                if len(doi) == 0:
                    doi = "none"
                if len(classification) == 0:
                    classification = "none"
                if len(author) == 0:
                    author = "none"
                if len(organization) == 0:
                    organization = "none"
                if not type(keywords)==list:
                    keywords = [keywords]
                if not type(author)==list:
                    author = [author]
                if not type(organization) == list:
                    organization = [organization]


                main_result.write(title + "\t")
                if keywords!="none":
                    for keyword_index in range(0, len(keywords)):
                        current_keyword = keywords[keyword_index].replace(";", "")
                        if keyword_index < len(keywords) - 1:
                            main_result.write(current_keyword + "&")
                        else:
                            main_result.write(current_keyword + "\t")
                else:
                    main_result.write(keywords + "\t")
                main_result.write(abstract + "\t")
                for author_index in range(0, len(author)):
                    current_author = author[author_index].replace(";", "")
                    if author_index < len(author) - 1:
                        main_result.write(current_author + "&")
                    else:
                        main_result.write(current_author + "\t")
                for organization_index in range(0, len(organization)):
                    current_organization = organization[organization_index].replace(";", "")
                    if organization_index < len(organization) - 1:
                        main_result.write(current_organization + "&")
                    else:
                        main_result.write(current_organization + "\t")
                main_result.write(doi + "\t")
                main_result.write(classification + "\n")


                reference = get_reference(article_url)
                print(reference)
                if len( reference["cankao"] )>0:#有参考文献
                    if not os.path.isdir(journal_month_path+"/参考文献"):
                        os.mkdir(journal_month_path+"/参考文献")
                    try:
                        refer_result = open( (journal_month_path+"/参考文献/%s.txt")%(title),"w" )
                        for refer in reference["cankao"]:
                            refer_result.write(refer+"\n")
                        refer_result.close()
                    except:
                        print("Title %s failed to save cankao."%(title))
                if len( reference["yinzheng"] ) >0:
                    if not os.path.isdir(journal_month_path+"/引证文献"):
                        os.mkdir(journal_month_path+"/引证文献")
                    try:
                        refer_result = open( (journal_month_path+"/引证文献/%s.txt")%(title),"w" )
                        for refer in reference["yinzheng"]:
                            refer_result.write(refer+"\n")
                        refer_result.close()
                    except:
                        print("Title %s failed to save cankao."%(title))
            main_result.close()
    print("over")