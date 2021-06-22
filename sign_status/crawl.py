#-*- coding: utf-8 -*-

import requests
import re
import json
import datetime
from bs4 import BeautifulSoup

def get_status():
    reply_list = []
    url = "http://www.kyonggi.ac.kr/boardView.kgu?bcode=B0077&id=331530&pid=34"
    res = requests.get(url)
    
    soup = BeautifulSoup(res.text, 'html.parser')
    all_reply_list = soup.select('.replyList form')
    
    for r in all_reply_list:
        raw = r.get_text()
        if "참여합니다" in raw:
            check_data = raw   
            if "-" in raw:  
                check_data = raw.split('-')[1]                                          
            if check_data not in reply_list:                                              
                reply_list.append(check_data)
    
    return len(reply_list)



def get_time():
    now = datetime.datetime.now()
    now_kr = now + datetime.timedelta(hours=9)
    return now_kr.strftime('%m/%d %H:%M')




cnt = get_status()


time = get_time()

new_data = {
        'time': time,
        'count': cnt
}

f_path = "/var/www/kgu/sign_status/data.json"

read_f = open(f_path, 'r')
old_status = json.load(read_f)
old_status.append(new_data)

write_f = open(f_path, 'w')
new_status = json.dumps(old_status)
write_f.write(new_status)

