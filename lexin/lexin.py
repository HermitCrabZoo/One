# -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import random


class LexinSport:
    def __init__(self, username, password, step):
        self.username = username
        self.password = password
        self.step = step

    # 登录
    def login(self):
        url = 'https://sports.lifesense.com/sessions_service/login?systemType=2&version=4.6.7'
        data = {'loginName': self.username, 'password': self.password,
                'clientId': '49a41c9727ee49dda3b190dc907850cc', 'roleType': 0, 'appType': 6}
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; LIO-AN00 Build/LIO-AN00)'
        }
        response_result = requests.post(url, data=json.dumps(data), headers=headers)
        status_code = response_result.status_code
        response_text = response_result.text
        # print('登录状态码：%s' % status_code)
        # print('登录返回数据：%s' % response_text)
        if status_code == 200:
            response_text = json.loads(response_text)
            user_id = response_text['data']['userId']
            access_token = response_text['data']['accessToken']
            return user_id, access_token
        else:
            return '登录失败'

    # 修改步数
    def change_step(self):
        # 登录结果
        login_result = self.login()
        if login_result == '登录失败':
            return '登录失败'
        else:
            url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?systemType=2&version=4.6.7'
            data = {'list': [{'DataSource': 2, 'active': 1, 'calories': int(self.step/4), 'dataSource': 2,
                              'deviceId': 'M_NULL', 'distance': int(self.step/3), 'exerciseTime': 0, 'isUpload': 0,
                              'measurementTime': time.strftime('%Y-%m-%d %H:%M:%S'), 'priority': 0, 'step': self.step,
                              'type': 2, 'updated': int(round(time.time() * 1000)), 'userId': login_result[0]}]}
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Cookie': 'accessToken=%s' % login_result[1]
            }
            response_result = requests.post(url, data=json.dumps(data), headers=headers)
            status_code = response_result.status_code
            # print('修改步数返回数据：%s' % response_text)
            print("Sync result: {}".format(response_result.text))
            if status_code == 200:
                return "Sync steps({}) succeed.".format(self.step)
            else:
                return "Sync steps({}) failure.".format(self.step)


# 睡眠到第二天执行修改步数的时间
def may_sleep_time():
    # 第二天日期
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # 第二天7点时间戳
    tomorrow_run_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) + 25200
    # print(tomorrow_run_time)
    # 当前时间戳
    current_time = int(time.time())
    # print(current_time)
    sleep_time = tomorrow_run_time - current_time
    time.sleep(sleep_time)


def start():
    while 1:
        step = random.randint(21537, 42671)
        for i in range(1, 4):
            try:
                # 修改步数结果
                print("Number {} times sync steps...".format(i))
                result = LexinSport('18316872434', '98b7ce537bfbaf709148ffd34a3abbfa', step).change_step()
                print(result)
                break
            except Exception as e:
                print("Number {} times sync steps error：{}".format(i, e))
        else:
            print("Sync steps failure.")
        # 睡眠
        may_sleep_time()


if __name__ == "__main__":
    start()
