import json
import os
import time
import random
import gc
import socket
socket.setdefaulttimeout(10) 
#import gevent
#from gevent import monkey; monkey.patch_all()
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
            #print(refer_page)
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
                    try:
                        refer_html = connectToReferencePage.connect_to_reference(ref_type=ref_type,page=refer_page)
                    except:
                        print("Faile to connect to page:%s"%(refer_page))
                        time.sleep(5)
                        continue
        except:
            print("Faile to connect to refer:%s"%(ref_type))
            continue
    return reference

def get_json_without_download( journal_type ):
    journal_json = json.load(open("./doc/%s.json"%(journal_type), "r",encoding="utf-8"))
    try:
        download_file = open( "./doc/%s_download.txt"%(journal_type), "r",encoding="utf-8" )
    except:
        print("There is no journal has been downloaded")
        pass
    for l in download_file.readlines():
        if l.replace("\n","").replace("\ufeff","") in journal_json:
            journal_json.pop( l.replace("\n","").replace("\ufeff","") )
        else:
            print("%s is not in %s"%(l,journal_type))
    return journal_json

def download_article(article_url,main_result,journal_type,journal_name,year,month,journal_year_path):
                    connectToArticlePage = connect_to_article.ConnectToAriclePage()
                    article_html = connectToArticlePage.article_page_connect(article_url)
                    connectToArticlePage.close()
                        #continue
                    articlePageParser = parse_article_page.ArticlePageParser()
                    if article_html == "None":
                        return False
                    articlePageParser.feed(article_html)
                    #print(data_list)
                    abstract = articlePageParser.get_abstract()
                    keywords = articlePageParser.get_keywords()
                    title = articlePageParser.get_title()
                    doi = articlePageParser.get_doi()
                    author = articlePageParser.get_author()
                    organization = articlePageParser.get_organization()
                    classification = articlePageParser.get_classification()
                    
                    if len(abstract) == 0:
                        abstract = "none"
                    if len(doi) == 0:
                        doi = "none"
                    if len(classification) == 0:
                        classification = "none"
                    if len(author) == 0:
                        author = ["none"]
                    if len(organization) == 0:
                        organization = ["none"]
                    write_data = ""
                    write_data += title + "\t"
                    if keywords == "none" or len(keywords)==0:
                        keywords = ["none"]
                    if type(keywords) != list:
                        keywords = [keywords]
                    if type(author) != list:
                        author = [author]
                    if type(organization) != list:
                        organization = [organization]
                    for keyword_index in range(0, len(keywords)):
                        current_keyword = keywords[keyword_index].replace(";", "")
                        if keyword_index < len(keywords) - 1:
                            write_data += (current_keyword + "&")
                        else:
                            write_data += (current_keyword + "\t")
                    write_data += (abstract + "\t")
                    for author_index in range(0, len(author)):
                        current_author = author[author_index].replace(";", "")
                        if author_index < len(author) - 1:
                            write_data += (current_author + "&")
                        else:
                            write_data += (current_author + "\t")
                    for organization_index in range(0, len(organization)):
                        current_organization = organization[organization_index].replace(";", "")
                        if organization_index < len(organization) - 1:
                            write_data += (current_organization + "&")
                        else:
                            write_data += (current_organization + "\t")
    
                    write_data += (doi + "\t")
                    write_data += (classification + "\n")
                    main_result.write(write_data)
    
                    reference = get_reference(article_url)
                    #print(reference)
                    time.sleep(random.uniform(0,1))
                    if len( reference["cankao"] )>0:#有参考文献
                        if not os.path.isdir(journal_month_path+"/参考文献"):
                            os.mkdir(journal_month_path+"/参考文献")
                        try:
                            refer_result = open( (journal_month_path+"/参考文献/%s.txt")%(title),"w",encoding="utf-8" )
                            for refer in reference["cankao"]:
                                refer_result.write(refer+"\n")
                            refer_result.close()
                        except:
                            print("Title %s failed to save cankao."%(title))
                    time.sleep(random.uniform(0,1))
                    if len( reference["yinzheng"] ) >0:
                        if not os.path.isdir(journal_month_path+"/引证文献"):
                            os.mkdir(journal_month_path+"/引证文献")
                        try:
                            refer_result = open( (journal_month_path+"/引证文献/%s.txt")%(title),"w",encoding="utf-8" )
                            for refer in reference["yinzheng"]:
                                refer_result.write(refer+"\n")
                            refer_result.close()
                        except:
                            print("Title %s failed to save cankao."%(title))
                    return True

if __name__=="__main__":
    journal_type = "哲学政法"
    #journal_type = "工业技术"
    all_journal_name = get_json_without_download( journal_type )
    journal_type_path = "../spyder_result/%s" % (journal_type)
    if not os.path.isdir(journal_type_path):
        os.mkdir( journal_type_path )
    
    for journal_name in list(all_journal_name.keys())[0: min( len(list(all_journal_name.keys())),1 )]:
            
        #journal_name = "电工材料"
        journal_path = (journal_type_path+"/%s") % (journal_name)
        try:
            version_of_journal = get_version_of_journal.get_version_of_journal(all_journal_name[journal_name])
        except:
            print("Cannot get version of %s"%(journal_name))
        if not os.path.isdir( journal_path ):
            os.mkdir( journal_path )
        log_result = open(journal_path+"/log.txt","a+")
        log_result.write(time.asctime( time.localtime(time.time()) )+"\n")
        log_result.close()
        for year in list(version_of_journal.keys()):#[0:1]:
            need_ignoe = False
            if journal_name == "军队政工理论研究":
                for ignore_year in range(2011,2018):
                    if str(ignore_year) in year:
                        need_ignoe = True
                        break
            if need_ignoe:
                continue
            log_result = open(journal_path+"/log.txt","a+")
            journal_year_path = (journal_path+"/%s") % (year)
            if not os.path.isdir(journal_year_path):
                os.mkdir(journal_year_path)
            for month in list(version_of_journal[year].keys()):#[0:1]:
                print("Journal_namee:%s --- Year:%s --- Month:%s --- Running time:%s\n"%(journal_name,year,month,time.asctime( time.localtime(time.time()) )))
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
                main_result = open(journal_month_path+"/检索结果.txt","w",encoding="utf-8")
                main_result.write("标题\t")
                main_result.write("关键词\t")
                main_result.write("摘要\t")
                main_result.write("作者\t")
                main_result.write("单位\t")
                main_result.write("DOI\t")
                main_result.write("分类号\n")
                
                url_thread = [] 
                for article_url in article_url_list:#[0:1]:
                #for article_url in ["http://d.wanfangdata.com.cn/Periodical/abjbtb201703003"]:
                    #print(article_url)
                    #url_thread.append( download_article(article_url,main_result,journal_type,journal_name,year,month,journal_year_path) ) 
                    download_article(article_url,main_result,journal_type,journal_name,year,month,journal_year_path)
                #gevent.joinall(url_thread)
                #del url_thread
                time.sleep(random.uniform(2,4))
                log_result.write( "Journal_namee:%s --- Year:%s --- Month:%s is over --- Running time:%s\n"%(journal_name,year,month,time.asctime( time.localtime(time.time()) )) )
                main_result.close()
            log_result.close()
            gc.collect()
        journal_download = open( "./doc/%s_download.txt"%(journal_type),"a+",encoding="utf-8")
        journal_download.write("%s\n"%(journal_name))
        journal_download.close()
    print("over")