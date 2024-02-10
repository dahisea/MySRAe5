import requests as req
import json
import sys
import time

CLIENT_SECRET = 'V378Q~w9Ox-guKNNF4Y0_zCjRIVwNwKbQLnzOduZ'
CLIENT_ID = 'c9c9ab50-df3c-4837-a8cc-f0320a7d9214'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
path = sys.path[0] + r'/temp.txt'

def get_refresh_token(client_id, client_secret):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    html = req.post(TOKEN_URL, data=data, headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    return refresh_token

def main():
    refresh_token = get_refresh_token(CLIENT_ID, CLIENT_SECRET)
    with open(path, 'w') as f:
        f.write(refresh_token)
    print('Refresh token saved to temp.txt')

if __name__ == "__main__":
    main()
