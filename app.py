#! /usr/bin/python
import requests
import os
import datetime

def Game_SG0_Sign(authorization):
    game_header = {
        'Authorization': authorization,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000730) NetType/WIFI Language/zh_CN'
    }

    r = requests.get('https://wx-api.youzu.com/game/374/welfare/sign-gift', headers=game_header)
    print('[少年三国志]', r.json())

    msg = r.json()['msg']
    ret = "少三0: " + msg + "\n"
    return ret

def Robot_Send(robot, msg):
    r = requests.post(robot, json={
        "msgtype": "text",
        "text": {
            "content": msg
        }
    })

    print('[机器人]', r.json())

def get_weather(api):
    r = requests.get('https://api.seniverse.com/v3/weather/daily.json?language=zh-Hans&unit=c&start=0&days=1&location=chongqing&key=' + api)

    day = r.json()['results'][0]['daily'][0]
    ret = day['low'] + '°C' + '~' + day['high'] + '°C' + ',' + day['text_day'] + day['text_night']

    print('[心知天气]', r.json())
    return '天气: ' + ret + '\n' \

def get_holiday(api, today):
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

def get_limit(today):
    weekday_s = today.strftime("%A")

    limit = ["周一: 1,6", "周二: 2,7", "周三: 3,8", "周四: 4,9", "周五: 5,0"]

    if weekday_s == 4:
        limit_s = "限行"
    else:
        limit_s = "不限行"

    weekday = today.weekday() + 1
    limit = '重庆限行: ' + limit_s + '(' + limit[weekday] + ')' + '\n'
    print('[重庆限行]', limit)
    return limit

def main():
    print('[Main] 开始执行')

    today = datetime.date.today()
    today_s = today.strftime("%Y-%m-%d")

    # SG
    authorization = os.environ["SG0_TOKEN"]
    sg0 = Game_SG0_Sign(authorization)

    # INFO
    # 心知天气 https://www.seniverse.com/
    xz_api = os.environ["XZ_API"]
    weather = get_weather(xz_api)

    # INFO
    # 天行数据 https://www.tianapi.com/
    tx_api = os.environ["TX_API"]
    holiday = get_holiday(tx_api, today)


    # ROBOT
    robot = os.environ["ROBOT"]

    # REPORT
    limit = get_limit(today)

    title = '====== ' + today_s + ' ======\n'
    result = title \
             + weather \
             + limit \
             + holiday \
             + sg0

    print(result)
    Robot_Send(robot, result)
    print('[Main] 脚本结束')

if __name__ == "__main__":
    main()