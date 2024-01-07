# -*- coding: UTF-8 -*-
import requests as req
import json, sys, time, random

path = sys.path[0] + r'/temp.txt'
num1 = 0

def gettoken(refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': id,
        'client_secret': secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    return access_token

def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    global num1
    localtime = time.asctime(time.localtime(time.time()))
    access_token = gettoken(refresh_token)
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    print('此次运行开始时间为 :', localtime)
    urls = [
        r'https://graph.microsoft.com/v1.0/me/drive/root',
        r'https://graph.microsoft.com/v1.0/me/drive',
        r'https://graph.microsoft.com/v1.0/drive/root',
        r'https://graph.microsoft.com/v1.0/users',
        r'https://graph.microsoft.com/v1.0/me/messages',
        r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        r'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        r'https://graph.microsoft.com/v1.0/me/drive/root/children',
        r'https://api.powerbi.com/v1.0/myorg/apps',
        r'https://graph.microsoft.com/v1.0/me/mailFolders',
        r'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
    ]
    for i, url in enumerate(urls):
        try:
            if req.get(url, headers=headers).status_code == 200:
                num1 += 1
                print(f"{i+1}调用成功{num1}次")
        except:
            print("pass")
            pass

for _ in range(6):
    main()
    for i in range(random.randint(100, 300), 0, -1):
        time.sleep(1)
