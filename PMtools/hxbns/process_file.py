import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json
import time
import os
from config.default import imagedir


class RequestsMethods(object):

    def __init__(self):
        self.cookie = dict(PHPSESSID='')

    def get_cookie(self):
        login_url = 'http://tw-hxbns.gm.funcell123.com/index.php?r=sys/user/login'
        cookie_request = requests.get(login_url)
        cookie_request.encoding = 'utf-8'
        cookies = dict(
            PHPSESSID=cookie_request.cookies['PHPSESSID'],
            dwz_theme=cookie_request.cookies['dwz_theme'],
            GAME_ID='173')
        # print(type(cookie_request.cookies['PHPSESSID']))
        self.cookie = cookies

    def get_validateCode(self):
        validatecode = 'http://tw-hxbns.gm.funcell123.com/index.php?r=site/verify/t/1452511909'
        login_r = requests.get(validatecode, cookies=self.cookie)
        i = Image.open(BytesIO(login_r.content))
        i.save(
            os.path.join(
                imagedir,
                'validateCode.png'),
            'png')

    def login(self):
        verify_value = input()
        login_upload = {
            'account': 'efun_service',
            'password': 'efun_service',
            'verify': verify_value}
        login_url = 'http://tw-hxbns.gm.funcell123.com/index.php?r=sys/user/login'
        login_r = requests.post(
            login_url,
            data=login_upload,
            cookies=self.cookie)
        login_r.encoding = 'utf-8'
        # print(login_r.text)

    def getcookie(self):
        return self.cookie

    def add_items(self, post_data):
        timestamp = str(int(time.time() * 1000))
        item_add_url = 'http://tw-hxbns.gm.funcell123.com/index.php?r=game/gm/mail/index&opt=add&_=' + timestamp
        add_respones = requests.post(
            item_add_url,
            data=post_data,
            cookies=self.cookie
        )
        add_respones.json()
        r_json = json.loads(add_respones.text)
        for a in r_json.keys():
            print(r_json[a])
        if r_json['statusCode'] == 200:
            return 'success'
        elif r_json['statusCode'] == 300:
            return r_json['message'].split('【')[1].split('】')[0]
        else:
            return 'unkown'


def read_send(file_path):
    rm = RequestsMethods()
    rm.get_cookie()
    rm.login()
    rm.select_server()

    with open(file_path, 'r', encoding='utf-8') as f:
        returnstr = ''
        for line in f:
            line = line.strip()
            if len(line.split('=')) == 2:
                tag, value = line.split('=')
                if tag == 'server':
                    serverid = value
                elif tag == 'mail_title':
                    mail_title = value
                elif tag == 'mail_content':
                    mail_content = value
                elif tag == 'goods_values':
                    goods_values = value
                    goods_list = goods_values.replace('，', ',').split(',')
                elif tag == 'player_list':
                    receiver_list = []
            elif len(line.split('=')) == 1:
                if line == '#':
                    post_dict = {}
                    goods_str = ''
                    for i in goods_list:
                        t = i.replace('：', ':').split(':')
                        t_name = t[0]
                        t_id = t[1]
                        t_num = t[2]
                        t_isbind = t[3]
                        good = {
                            "goods_id": t_id,
                            "goods_num": t_num,
                            "goods_bind": t_isbind,
                            "goods_name": t_name}
                        goods_str = goods_str + str(good) + '|'
                    post_dict['goods_values'] = goods_str[:-1]
                    post_dict['mail_title'] = mail_title
                    post_dict['mail_content'] = mail_content
                    receiver_str = ''
                    for i in receiver_list:
                        receiver_str = receiver_str + i + ','
                    post_dict['player_list'] = receiver_str

                    post_dict['callbackType'] = 'closeCurrent'
                    post_dict['platform'] = '-1'
                    post_dict['sendmode'] = 'roleName'
                    post_dict['item_name'] = ''
                    post_dict['item_id'] = ''
                    post_dict['selected_item_id'] = ''
                    post_dict['server'] = serverid

                    response = rm.send_prize(post_dict)
                    if response == "<script>alert('待审批邮件添加成功!');</script>":
                        returnstr = returnstr + \
                            str(serverid) + '区奖励提交完毕' + '\n'
                        #print(str(serverid) + '区奖励提交完毕')
                    else:
                        returnstr = returnstr + \
                            str(serverid) + '区奖励提交失败' + '\n'
                        #print(str(serverid) + '区奖励提交失败')
                    commited = rm.commited_id()
                    commited_list = [
                        x for x in commited.split(',') if x != '']
                    different_list = [
                        x for x in receiver_list if x not in commited_list]
                    for x in different_list:
                        returnstr = returnstr + x + '\n'
                    # print(different_list)

                    receiver_list = []
                else:
                    receiver_list.append(line)

            else:
                returnstr += '输入参数有误'
                # print('输入参数有误')
    return returnstr
