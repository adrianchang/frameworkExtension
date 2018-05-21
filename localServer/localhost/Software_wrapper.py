# -*- coding: UTF-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time
import sqlite3

class Software:
    # @name: name of the software 
    # @local_ver: version number of the local software 
    # @url: normal url of the software on www.softpedia.com
    # @version_rex: regular expression to search for version number in plain text
    # @db_cursor: cursor Object of a sqlite3 database
    # @special: flag, 1 indicates url not on SOFTPEDIA, 0 otherwise 
    # @special_func: function used to scrape version number of the software
    #                if @special == 1
    #  
    def __init__(self, name, local_ver, url, version_rex, db_conn=None,
        special=0, special_func=None):

        self.name = name
        self.local_ver = local_ver
        self.latest_ver = None 
        self.version_rex = version_rex
        self.db_cursor = None
        if db_conn:
            self.db_cursor = db_conn.cursor()
        self.url = url 
        self.special = special 
        self.special_func = special_func 
    
    # Scrape data from webpages 
    # def ScrapeVersionInfo(self):
    #     # avoid being blocked
    #     time.sleep(0.2)
    #     if self.special == 0:
    #         headers={
    #             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    #         }
    #         response = requests.get(self.url, headers=headers)
    #         content = response.content
    #         f = open('test.html','wb')
    #         f.write(content)

    #         soup = BeautifulSoup(content, 'html.parser')
    #         # there are two formats/kinds of tags
    #         elem = soup.findall()
    #         print(elem)
            
    #         if not elem:
    #             elem = soup.find('div',attrs={'class':'multiline'}, text=re.compile(self.version_rex))
    #         text = elem.text
    #         print(text)
    #         self.latest_ver = ".".join(re.search(self.version_rex, text, re.M).groups())
            
    #     else:
    #         self.latest_ver = self.special_func()

            
    def ScrapeVersionInfo(self):
        # avoid being blocked
        time.sleep(0.2)
        if self.special == 0:
            headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
            }
            response = requests.get(self.url, headers=headers)
            content = response.content
            f = open('test.html','wb')
            f.write(content)
            f = open('test.html','r')
            res = re.search(self.version_rex,f.read()).groups()
            self.latest_ver = ".".join(res)

            




    # Assume version number follow the pattern x.x.x[.x...]   
    # 1 indicates there is an update 
    def CompareVersion(self):
        try:
            local_list = self.local_ver.split('.')
            latest_list = self.latest_ver.split('.')
            return local_list < latest_list 
        except Exception as e:
            print(e) 
            return 0
    # ./data/software.db
    def DumpToDB(self,db_cursor, name, old, new):
        db_cursor.execute('INSERT INTO Software VALUES (?,?,?)',[name, old, new])
    
    def ReadFromDB(self, db_cursor, name):
        return db_cursor.execute("SELECT * FROM Software WHERE name=?",name)[0]
        
    

    def CheckUpdate(self):
        if self.db_cursor:
            name, self.local_ver, self.latest_ver = self.ReadFromDB(self.db_cursor, self.name)
        return self.CompareVersion()


# version_rex = '(\d+)\.(\d+)\.(\d+)\.(\d+)'
# #response = requests.get(self.url)
# #content = response.content
# content = open('test.html','r',encoding='utf-8')
# soup = BeautifulSoup(content, 'html.parser')
# # there are two formats/kinds of tags
# elem = soup.find('h2',class_="sanscond",text= re.compile(version_rex))
# if not elem:
#     elem = soup.find('div',attrs={'class':'multiline'}, text= re.compile(version_rex))
# text = elem.text
# print(text)
# latest_ver = ".".join(re.search(version_rex, text, re.M).groups())
# print(latest_ver)
# f = open('test.html','r',encoding='utf-8')
# res = re.search('(\d+)\.(\d+)\.(\d+)\.(\d+)',f.read()).groups()
# print(res)

# soft = Software('Google Chrome', '65.0.3325.181', 'http://www.softpedia.com/get/Internet/Browsers/Google-Chrome.shtml', r'(\d+)\.(\d+)\.(\d+)\.(\d+)')
# soft.ScrapeVersionInfo()
# print(soft.latest_ver)