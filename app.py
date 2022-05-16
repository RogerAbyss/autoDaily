#coding=utf-8
#! /usr/bin/python
import re

import requests
import os
import datetime

# ======= Function =======
# 1. 获取假期数据
# 2. 获取天气数据
# 3. 获取车辆限行规则
# 4. 机场签到
# ========================

# ====== Enviroment ======
# os.environ
# TX_API        [假期]https://www.tianapi.com/
# XZ_API        [天气]https://www.seniverse.com/
# email
# ========================

debug=False

def get_enviroment(key):
    """
    获取环境变量,
    debug下从本地config.py中获取
    否则则从github环境变量中获取
    :param key:
    :return:
    """
    if debug:
        import config as config
        return config.env[key]
    else:
        return os.environ.get(key)

def get_weather(api, city='chongqing'):
    """
    获取天气情况
    :param api:
    :return:
    """
    r = requests.get('https://api.seniverse.com/v3/weather/daily.json?language=zh-Hans&unit=c&start=0&days=1&location=' + city + '&key=' + api)

    day = r.json()['results'][0]['daily'][0]
    ret = day['low'] + '°C' + '~' + day['high'] + '°C' + ',' + day['text_day'] + day['text_night']

    print('[心知天气]', r.json())
    return '天气: ' + ret + '\n' \

def get_holiday(api):
    """
    获取假期情况
    :param api:
    :return:
    """
    today = datetime.date.today()

    r = requests.get('http://api.tianapi.com/txapi/jiejiari/index', params={
        "date": today.strftime("%Y-%m"),
        "type": "2",
        "key": api
    })

    days = r.json()['newslist']
    holiday = ''

    for day in days:
        if len(day['holiday']) > 0:
            holiday = day['name'] + ': ' + day['tip'] + '\n'
            break

    print('[天行数据]', r.json())
    return holiday

def get_limit():
    """
    获取车辆限行规则, 目前规则----29L0
    :param today:
    :return:
    """
    today = datetime.date.today()

    limit = ["周一: 1,6", "周二: 2,7", "周三: 3,8", "周四: 4,9", "周五: 5,0", "周六: 不限行", "周日: 不限行", "ERROR", "ERROR"]

    if today.weekday() == 4:
        limit_s = "限行"
    else:
        limit_s = "不限行"

    weekday = today.weekday()
    limit = '重庆限行: ' + limit_s + '(' + limit[weekday] + ')' + '\n'
    print('[重庆限行]', limit)
    return limit

def send_email(message, password):
    if debug:
        print("[邮件] 不发送邮件")
        return

    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    import re

    sender = 'roger_ren@qq.com'
    receiver = '492764029@qq.com'
    smtpserver = 'smtp.qq.com'

    msg = MIMEText(str(message), 'plain', 'utf-8')
    msg['Subject'] = Header('Github-Daily', 'utf-8')
    msg['to'] = receiver
    msg['from'] = sender

    server = smtplib.SMTP_SSL(smtpserver)
    for _ in range(10):
        try:
            server.login(receiver, password)
            server.sendmail(sender, receiver, msg.as_string())
            print("[邮件] 发送成功")
            break
        except:
            print("[邮件] 发送失败")
    server.quit()

def setup_report(list):
    content = ''
    for each in list:
        content += each

    print('===========')
    print(content)
    print('===========\n')
    return content

def auto_sign_youyun666(email, passwd):
    import requests
    from urllib.parse import quote
    from bs4 import BeautifulSoup

    # 登录
    api_login = 'https://youyun222.net/auth/login?email=' + quote(email) + '&passwd=' + passwd
    res_login = requests.request("POST", api_login)
    print('[优云666] 登录:\n', res_login.json())

    # 签到
    api_sign = 'https://youyun222.net/user/checkin'
    res_sign = requests.request("POST", api_sign, cookies=res_login.cookies)

    print('[优云666] 签到:\n', res_sign.json())

    sign_ret = '\n' + '自动签到:[优云666] ' + '<' + email + '>' + res_sign.json()['msg'] + '\n'

    # 详情
    api_user = 'https://youyun222.net/user'
    res_user = requests.request("GET", api_user, cookies=res_login.cookies)

    soup = BeautifulSoup(res_user.content, features="html.parser")

    try:
        scripts = soup.find_all("script")
        ret = str(re.findall(r'window.ChatraIntegration.*var userUUID', str(scripts), re.S)[0])

        ret = ret.replace('window.ChatraIntegration =', '')
        ret = ret.replace('var userUUID', '')
        ret = ret.replace('\n', '')
        ret = ret.replace(' ', '')

        print(ret)
        sign_ret = sign_ret + ret + '\n'

    except AttributeError:
        print("[优云666] 抓取流量错误")

    return sign_ret

def main():
    print('[Main] 开始执行')

    # Get Enviroment: os.environ
    xz_api = get_enviroment("XZ_API")
    tx_api = get_enviroment("TX_API")
    email_token = get_enviroment('EMAIL')
    youyun666_email1 = get_enviroment("YOUYUN_ID1")
    youyun666_email2 = get_enviroment("YOUYUN_ID2")
    youyun666_pwd = get_enviroment("YOUYUN_PWD")


    weather = get_weather(xz_api)
    holiday = get_holiday(tx_api)

    # REPORT
    limit = get_limit()

    sign_ret1 = auto_sign_youyun666(youyun666_email1, youyun666_pwd)
    sign_ret2 = auto_sign_youyun666(youyun666_email2, youyun666_pwd)

    message = setup_report([weather, holiday, limit, sign_ret1, sign_ret2])
    send_email(message, email_token)
    print('[Main] 脚本结束')

if __name__ == "__main__":
    main()
