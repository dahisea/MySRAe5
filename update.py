# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import time
from cryptography.hazmat.primitives import serialization # 导入cryptography库中的serialization模块
from cryptography.hazmat.primitives.asymmetric import padding # 导入cryptography库中的padding模块
from cryptography.hazmat.primitives import hashes # 导入hashes模块

















# Register an Azure app first, ensure the app has the following permissions:
# files: Files.Read.All, Files.ReadWrite.All, Sites.Read.All, Sites.ReadWrite.All
# user: User.Read.All, User.ReadWrite.All, Directory.Read.All, Directory.ReadWrite.All
# mail: Mail.Read, Mail.ReadWrite, MailboxSettings.Read, MailboxSettings.ReadWrite
# After registration, be sure to click the button representing xxx to grant admin consent; otherwise, the Outlook API cannot be invoked.

# Define the file path
path = sys.path[0] + r'/temp.txt'
# Define the public key path
public_key_path = sys.path[0] + r'/public_key.pem'

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
    # Return the new token
    return refresh_token, access_token

# Define the function to encrypt the token
def encrypt(token):
    # Read the public key from the file
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())
    # Encrypt the token with the public key
    encrypted_token = public_key.encrypt(token.encode(), padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))
    # Return the encrypted token
    return encrypted_token

# Define the function to write the encrypted token to the file
def write(encrypted_token):
    # Write the encrypted token to the file
    with open(path, 'wb+') as f:
        f.write(encrypted_token)

# Define the main function
def main():
    # Open the file
    with open(path, "r+") as fo:
        # Read the file content
        refresh_token = fo.read()
    # Call the function to get the token
    refresh_token, access_token = gettoken(refresh_token)
    # Call the function to encrypt the token
    encrypted_token = encrypt(access_token)
    # Call the function to write the encrypted token to the file
    write(encrypted_token)

# Execute the main function
main()
