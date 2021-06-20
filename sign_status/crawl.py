#-*- coding: utf-8 -*-

import requests
import re
import json
import datetime

def get_status():
    url = "http://www.kyonggi.ac.kr/boardView.kgu?bcode=B0077&id=331530&pid=34"
    res = requests.get(url)
    raw = res.text

    pattern = r"참여합니다"
    find_res = re.findall(pattern, raw)
    
    return len(find_res)

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

