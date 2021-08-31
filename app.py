#! /usr/bin/python
import requests
import os
import time

def Game_SG0_Sign(authorization):
    game_header = {
        'Authorization': authorization,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x18000730) NetType/WIFI Language/zh_CN'
    }

    r = requests.get('https://wx-api.youzu.com/game/374/welfare/sign-gift', headers=game_header)
    print(r.json())
    return r.json()['msg']

def Robot_Send(robot, msg):
    r = requests.post(robot, json={
        "msgtype": "text",
        "text": {
            "content": msg
        }
    })

    print(r.json())

def main():
    print('开始执行')
    authorization = os.environ["SG0_TOKEN"]
    sg0 = Game_SG0_Sign(authorization)

    robot = os.environ["ROBOT"]

    localtime = time.asctime( time.localtime(time.time()) )
    result = "====== 执行结果 ======\n" + localtime + "\n" + "====================\n" + "少年三国志: " + sg0 + "\n"
    Robot_Send(robot, result)

if __name__ == "__main__":
    main()