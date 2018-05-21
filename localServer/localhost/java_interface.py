import sys
import pandas as pd
import csv
from Software_wrapper import Software
import re
import sys

# @whitelist: dict of software whitelist
#  format: {"name":{"url":...,"regex":"..."},...}
# @softwares: list of software names
# 
# return: soft_obj, a list of Software objects
def search_whitelist(white_list, softwares, db_conn=None):
    soft_obj = []
    for local_soft in softwares:
        for soft in white_list:
            if soft.lower() in local_soft.lower():
                try:
                    name = local_soft
                    # hard code local version since we don't have to return local version
                    local_ver = "0.0.0.0"
                    url = white_list[soft]['url']
                    version_rex = white_list[soft]['regex']
                    # NO DATABASE USED NOW
                    soft_obj.append(Software(name, local_ver, url, version_rex))
                except Exception as e:
                    print("Get %s full info failed"%(soft))
                    print(e)
    return soft_obj



                

def fetch_version(
        white_list,
        soft_list
    ):
    soft_obj_list = search_whitelist(white_list, soft_list)

    for software in soft_obj_list:
        #try:
        software.ScrapeVersionInfo()
        print(software.name + '->' + software.latest_ver)
        #except Exception as e
            #print(e) 
    return None


white_list = { 
       "Chrome":{
        "url":"http://www.softpedia.com/get/Internet/Browsers/Google-Chrome.shtml", 
        "regex":"(\d+)\.(\d+)\.(\d+)\.(\d+)",
    },
    "VMware Player":{
        "url":"http://www.softpedia.com/get/System/OS-Enhancements/VMware-Player.shtml",
        "regex":"(\d+)\.(\d+)\.(\d+)\s+Build\s+(\d+)"
    },
    "Xshell":{
        "url":"http://www.softpedia.com/get/Network-Tools/Telnet-SSH-Clients/Xshell.shtml",
        "regex":"(\d+)\.(\d+)\s+Build\s+(\d+)"

    },
    "IntelliJ IDEA":{
        "url":"http://www.softpedia.com/get/Programming/Coding-languages-Compilers/IntelliJ-IDEA.shtml",
        "regex":"(\d+)\.(\d+)\.(\d+)\s+Build\s+(\d+)\.(\d+)\.(\d+)"

    },
    "TeamViewer":{
        "url":"http://www.softpedia.com/get/Internet/Remote-Utils/TeamViewer.shtml",
        "regex":"(\d+)\.(\d+)\.(\d+)"
    },
    "LINE":{
        "url":"http://www.softpedia.com/get/Mobile-Phone-Tools/Others/Naver-LINE.shtml",
        "regex":"(\d+)\.(\d+)\.(\d+)\s+Build\s+(\d+)"
    },
    "Skype":{
        "url":"http://www.softpedia.com/get/Office-tools/Fax-Telephony/Skype.shtml",
        "regex":"Skype\s+(\d+)\.(\d+)\.(\d+)\.(\d+)"
    }
}


soft_list = sys.argv[1:]
fetch_version(white_list, soft_list)
    



