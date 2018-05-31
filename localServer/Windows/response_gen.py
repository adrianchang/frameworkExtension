import sys
import pandas as pd
import csv
from Software_wrapper import Software
import re
import json 

# read csv files into Dataframe and merge them
# and remove rows with invalid version number
def parse_csv(csv_files=[
        r'.\data\version1.csv',
        r'.\data\version2.csv'
    ]):

    info_table = pd.concat([pd.read_csv(f) for f in csv_files])
    #print(info_table) #DEBUG
    return info_table[pd.notnull(info_table['DisplayVersion'])]

# @whitelist: dict of software whitelist
#  format: {"name":{"url":...,"regex":"..."},...}
# @softwares: Dataframe of local softwares' info
# 
# return: soft_obj, a list of Software objects
def search_whitelist(white_list, softwares, db_conn=None):
    soft_obj = []
    for index, row in softwares.iterrows():
        for soft in white_list:
            if soft.lower() in row['DisplayName'].lower() :
                try:
                    name = row['DisplayName']
                    local_ver = row['DisplayVersion']
                    assert local_ver
                    url = white_list[soft]['url']
                    version_rex = white_list[soft]['regex']
                    # NO DATABASE USED NOW
                    soft_obj.append(Software(name, local_ver, url, version_rex))
                except Exception as e:
                    print("Get %s full info failed"%(soft))
                    print(e)
    return soft_obj



                

def generate_response(
        csv_files=[
        r'.\data\version1.csv',
        r'.\data\version2.csv'
        ] 
    ):
    local_soft = parse_csv(csv_files)
    with open(r'.\data\white_list.json') as f:
        white_list = json.load(f)
        
    soft_obj_list = search_whitelist(white_list, local_soft)
    packet = {
        "os": "windows",
        "softwares": []
    }

    for software in soft_obj_list:
        #try:
        software.ScrapeVersionInfo()
        packet["softwares"].append({
        "name":software.name,
        "old_version": software.local_ver,
        "new_version": software.latest_ver,
        "id": 0,
        "updatable":"false",
    })
        #except Exception as e:
            #print(e)
    return packet

#### Unit test ####
'''
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
    }
}  
'''
# packet = generate_response(white_list)
# print(packet)




