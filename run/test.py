# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import time
import random
import base64

path = sys.path[0] + '/temp.txt'

# Define successful call count
numa = 0

# Define client id and secret (replace with your actual values)



# Define the function to get a token
def get_token(refresh_token):
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

# Define the function to test API availability
def main():
    with open(path, "r+") as fo:
        encoded_refresh_token = fo.read()
        refresh_token = base64.b64decode(encoded_refresh_token).decode('utf-8')

    global numa
    localtime = time.asctime(time.localtime(time.time()))
    access_token = get_token(refresh_token)
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    print('This run started at:', localtime)
    urls = [
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/drive/root',
        'https://graph.microsoft.com/v1.0/users',
        'https://graph.microsoft.com/v1.0/me/messages',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/drive/root/children',
        'https://api.powerbi.com/v1.0/myorg/apps',
        'https://graph.microsoft.com/v1.0/me/mailFolders',
        'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
    ]

    for i, url in enumerate(urls):
        try:
            if req.get(url, headers=headers).status_code == 200:
                numa += 1
                print(f"{i+1} Call successful {numa} times")
        except:
            print("pass")
            pass

# Execute 6 times
for _ in range(6):
    main()
    time.sleep(random.randint(100, 300))
