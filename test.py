import requests as req
import json
import sys
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Define file paths
private_key_path = sys.path[0] + '/private_key.pem'
token_path = sys.path[0] + '/temp.txt'
num1 = 0

def load_private_key():
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def decrypt_token(encrypted_token, private_key):
    token = private_key.decrypt(
        encrypted_token,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=padding.MGF1.ALGORITHM.SHA256),
            algorithm=padding.OAEPAlgorithm.SHA256,
            label=None
        )
    )
    return token.decode()

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

def main():
    private_key = load_private_key()
    with open(token_path, "rb") as fo:
        encrypted_token = fo.read()
    refresh_token = decrypt_token(encrypted_token, private_key)

    global num1
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
                num1 += 1
                print(f"{i+1} Call successful {num1} times")
        except:
            print("pass")
            pass

for _ in range(6):
    main()
    time.sleep(random.randint(100, 300))
