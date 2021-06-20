#-*- coding:utf-8 -*-

import requests, html
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

class Sign:
    def __init__(self):
        self.session = requests.session()
        self.name = ''
        self.major = ''

    def login(self, user_id, user_pw):
        url = "https://www.kyonggi.ac.kr/HSSOLogin.kgu?mzcode=K00M0500"
        data = {'id': user_id, 'passwd': user_pw, 'mzcode': 'K00M0500'}
        res = self.session.post(url, data=data)
        
        if "일치하지 않습니다" in res.text:
            return (False, "아이디 또는 비밀번호가 일치하지 않습니다")
        elif "비활성화 되었습니다" in res.text:
            return (False, "계정이 비활성화 되어있습니다. KUTIS에서 비밀번호 초기화 후 다시 시도해주세요.")
        
        return (True, '')

    def get_info(self):
        url = "http://kutis.kyonggi.ac.kr/webkutis/filter/deviceSSOCheck.jsp"
        res = self.session.get(url)

        if "로그인 영역" in res.text:
            return (True, "KUTIS에서 학번 및 이름 정보를 받아오지 못했습니다. 관리자에게 문의하세요.")

        soup = BeautifulSoup(res.text, 'html.parser')
        self.major = soup.select_one('header #memInfo dd:nth-child(2)').get_text().replace(': ', '')
        self.name = soup.select_one('header #memInfo dd:nth-child(6)').get_text().replace(': ', '')

        return (True, )

    def sign(self):
        url = "https://www.kyonggi.ac.kr/boardAppendSave.kgu"

        message = f"서명 운동에 참여합니다. - {self.major} {self.name}"

        data = {
            'bcode': 'B0077',
            'id': '331530',
            'pid': '34',
            'boardAppend.pid': '331530',
            'lgF': '1',
            'pF': '1',
            'boardAppend.comments': message
        }
        res = self.session.post(url, data=data)

        
        if message in res.text:
            return (True, message)

        return (False, "알 수 없는 이유로 서명을 실패했습니다. 관리자에게 문의하세요.")


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/sign', methods=['POST'])
def sign():
    sign = Sign()
    user_id = request.form.get('id')
    user_pw = request.form.get('pw')

    if len(user_id) + len(user_pw) < 5:
        return render_template('err.html', msg="아이디와 비밀번호를 확인하세요")

    login = sign.login(user_id, user_pw)

    if login[0]:
        info = sign.get_info()
        if info[0]:
            msg = sign.sign()
            if msg[0]:
                return render_template('signed.html', msg=msg[1])
            else:
                return render_template('err.html', msg=msg[1])
        else:
            return render_template('err.html', msg=info[1])
    else:
        return render_template('err.html', msg=login[1])


@app.route('/code')
def code():
    raw_code = open("/var/www/kgu/simple_sign/sign.py", 'r', encoding='utf-8').read()
    return '\x3cpre\x3e\x3ccode\x3e'+raw_code+'\x3c/code\x3d\x3c/pre\x3e'

if __name__ == '__main__':
    app.run('0.0.0.0', port=10002)
