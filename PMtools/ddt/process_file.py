import requests
from bs4 import BeautifulSoup
import multiprocessing
import time
import re


class RequestsMethods(object):

    def __init__(self):
        self.cookie = dict(PHPSESSID='')

    def get_cookie(self):
        login_url = 'http://113.196.57.124/login.php'
        cookie_request = requests.get(login_url)
        cookie_request.encoding = 'utf-8'

        # print(type(cookie_request.cookies['PHPSESSID']))
        self.cookie = dict(PHPSESSID=cookie_request.cookies['PHPSESSID'])

    def login(self):
        login_upload = {
            'user_name': '8888play',
            'password': '8888play2015',
            'language': 'cn',
            'loginSubmit': '登录'}
        login_url = 'http://113.196.57.124/login.php'
        login_r = requests.post(
            login_url,
            data=login_upload,
            cookies=self.cookie)
        login_r.encoding = 'utf-8'
        # print(login_r.text)

    def select_server(self, server_code=2000003):
        select_url = 'http://113.196.57.124/server/server.php?DB_selected=' + \
            str(server_code)
        response = requests.get(select_url, cookies=self.cookie)
        response.encoding = 'utf-8'
        # print(response.text)
        # print(login_r.text)

    def cookiep(self):
        return self.cookie

    def send_prize(self, post_data):
        item_add_url = 'http://113.196.57.124/playerEmail/playerEmail_option.php?option=add'
        add_respones = requests.post(
            item_add_url,
            data=post_data,
            cookies=self.cookie
        )
        add_respones.encoding = 'utf-8'
        return add_respones.text

    def commited_id(self):
        checklist_url = 'http://113.196.57.124/playerEmail/playerEmail_chklist.php'
        checklist_respone = requests.get(checklist_url, cookies=self.cookie)
        checklist_respone.encoding = 'utf-8'
        soup = BeautifulSoup(checklist_respone.text, "html.parser")
        soup.encoding = 'utf-8'
        # print(soup.text)
        names = soup.table.find_all('tr')[1].find_all('td')[2].text.strip()
        return names


def read_send(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        returnstr = ''
        requestlist = []
        for line in f:
            line = line.strip()
            if len(line.split('=')) == 2:
                tag, value = line.split('=')
                if tag == 'serverid':
                    serverid_list = value.replace('，', ',').split(',')
                elif tag == 'title':
                    title = value
                elif tag == 'body':
                    body = value
                elif tag == 'att_items':
                    items_list = value
                elif tag == 'receiver':
                    receiver_value = value
                    receiver_list = []
            elif len(line.split('=')) == 1:
                if line == '#':
                    post_dict = {}
                    post_dict['att_items'] = items_list
                    post_dict['title'] = title
                    post_dict['body'] = body
                    if receiver_value != 'all':
                        post_dict['to_all'] = '0'
                        receiver_str = ''
                        for i in receiver_list:
                            receiver_str = receiver_str + i + '\n'
                        if re.match(
                                r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}',
                                receiver_str):
                            post_dict['receiver_id'] = receiver_str
                            post_dict['receiver'] = ''
                        else:
                            post_dict['receiver_id'] = ''
                            post_dict['receiver'] = receiver_str
                    else:
                        post_dict['to_all'] = '1'
                        post_dict['receiver'] = ''
                        post_dict['receiver_id'] = ''

                    post_dict['add_att'] = '1'
                    post_dict['next'] = ''
                    for serverid in serverid_list:
                        requestlist.append((post_dict, serverid))
                    receiver_list = []
                else:
                    receiver_list.append(line)

            else:
                returnstr += '输入参数有误'
                # print('输入参数有误')
        results = []
        pool_size = multiprocessing.cpu_count()
        print(pool_size)
        pool = multiprocessing.Pool(pool_size)  # 设置线程池大小
        results = pool.map(requestlist_post, requestlist)
        for restr in results:
            returnstr = returnstr + restr
    return returnstr


def requestlist_post(requesttuple):
    rm = RequestsMethods()
    rm.get_cookie()
    rm.login()
    rm.select_server(requesttuple[1])

    response = rm.send_prize(requesttuple[0])
    if response == "<script>alert('待审批邮件添加成功!');</script>":
        returnstr = str(requesttuple[1]) + '区奖励提交完毕' + '\n'
        #print(str(serverid) + '区奖励提交完毕')
    else:
        returnstr = str(requesttuple[1]) + '区奖励提交失败' + '\n'
        #print(str(serverid) + '区奖励提交失败')
    if re.match(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', requesttuple[0]['receiver_id']) is None:
        commited = rm.commited_id()
        commited_list = [
            x for x in commited.split(',') if x != '']
        print(requesttuple[1])
        different_list = [x for x in requesttuple[0][
            'receiver'].split('\n') if x not in commited_list]
        for x in different_list:
            returnstr = returnstr + x + '\n'
        print(different_list)
    return returnstr
