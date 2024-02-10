import requests as req
import json
import sys
import time
import random
import base64

path = sys.path[0] + '/temp/temp.txt'

# Define client id and secret (replace with your actual values)






# Define successful call count
num_successful_calls = 0

# Define the function to get an access token
def get_access_token(refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }
    response = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    json_data = json.loads(response.text)
    new_refresh_token = json_data['refresh_token']
    access_token = json_data['access_token']
    return access_token

# Define the function to test API availability
def test_api_availability():
    try:
        global num_successful_calls
        with open(path, "r+") as file:
            base64_encoded_refresh_token = file.read()
            refresh_token = base64.b64decode(base64_encoded_refresh_token).decode('utf-8')

        localtime = time.asctime(time.localtime(time.time()))
        access_token = get_access_token(refresh_token)
        headers = {'Authorization': f"Bearer {access_token}", 'Content-Type': 'application/json'}
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
            response = req.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            print(f"{i+1}. Call to {url} successful ({num_successful_calls + 1} successful calls in total)")
            num_successful_calls += 1

    except Exception as e:
        print(f"Error occurred: {e}")

# Execute 6 times with random intervals
for _ in range(6):
    test_api_availability()
    time.sleep(random.randint(100, 300))
