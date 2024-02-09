# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import time
import rsa












# Define the file paths
path = sys.path[0] + r'/temp.txt'
public_key_path = sys.path[0] + r'/public_key.txt'

# Define the function to get the token
def gettoken(refresh_token):
    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': id,
        'client_secret': secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    # Send a post request
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    jsontxt = json.loads(html.text)
    # Get the new token
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    # RSA encrypt the access_token
    with open(public_key_path, "rb") as key_file:
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
        encrypted_token = rsa.encrypt(access_token.encode(), public_key)
    # Write the encrypted token to the file
    with open(path, 'wb') as f:
        f.write(encrypted_token)

# Define the main function
def main():
    # Open the file
    with open(path, "r+") as fo:
        # Read the file content
        refresh_token = fo.read()
    # Call the function to get the token
    gettoken(refresh_token)

# Execute the main function
main()
