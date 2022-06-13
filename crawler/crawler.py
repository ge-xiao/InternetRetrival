# -*- coding: UTF-8 -*-

import re
import requests


def download(url, retry_count=1):
    html = None
    for retry in range(retry_count):
        print(f'Downloading : {url}')
        custom_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        try:
            r = requests.get(url, headers=custom_headers, verify=False)
            if r.status_code == 200:
                print('status_code : {0}'.format(r.status_code))
                html = r.text  # html = r.content
            else:
                print('status_code : {0}'.format(r.status_code))
            break
        except BaseException as ex:
            print(f'Download error : {ex}')
    return html


import os
from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
import pandas as pd
import json
if __name__ == "__main__":

    #temp_url = r'http://gswen.cn/poetry/750.html'
    contents=[]
    titles=[]
    authors=[]
    dynastys=[]
    for i in range(1,1100,1):
        try:
            print("========="+str(i)+"=========")
            temp_url = r'http://gswen.cn/poetry/'+str(i)+".html"
            #temp_url = r'http://gswen.cn/poetry/7.html'

            sitemap = download(temp_url)
            soup = BeautifulSoup(sitemap,"html.parser",from_encoding="utf-8")
            content_main=soup.find_all("dl", "content")[0]
            content = ""
            #去重操作
            content_list=[]
            for cd in content_main.dd.descendants:
                #print(cd.contents)
                if cd.string!=None and len(cd.string)>1:
                    sub_str=cd.string
                    sub_str=sub_str.replace('\n',"").replace(" ","")
                    content_list.append(sub_str)
            content_list=list(set(content_list))
            for i in content_list:
                content+=i
            article = soup.find_all("div", "article")[0]
            title=article.h1.string
            author=article.contents[3].find("div","f-l").contents[1].string
            dynasty=article.contents[3].find("div","f-l").contents[3].string

            #contents.append(json.dumps(content,ensure_ascii=False))
            contents.append(content)
            titles.append(title)
            dynastys.append(dynasty)
            authors.append(author)
        except:
            print("erro")
    data={
        "title":titles,
        "author":authors,
        "dynasty":dynastys,
        "content":contents
    }
    df=pd.DataFrame(data)
    print(df)
    df.to_csv("data.csv",encoding='utf_8_sig')
