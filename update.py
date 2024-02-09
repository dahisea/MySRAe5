import requests as req
import json
import sys
import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding # 修改了这一行，导入了正确的 padding 模块
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes








# Define the file paths
public_key_path = sys.path[0] + r'/public_key.pem'
token_path = sys.path[0] + r'/temp.txt'

def get_public_key():
    # Load the public key from the file
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def encrypt_with_public_key(token, public_key):
    # Encode the token to base64
    token = base64.b64encode(token.encode())
    # Encrypt the token with the public key using OAEP padding
    cipher_text = public_key.encrypt(
        token,
        padding.OAEP( # 修改了这一行，使用了 OAEP 类，而不是属性
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text

def request_token(refresh_token):
    try:
        # Set the headers and data for the POST request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': id,
            'client_secret': secret,
            'redirect_uri': 'http://localhost:53682/'
        }
        # Send the POST request to the token endpoint
        html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
        # Raise an exception if the status code is not 200
        html.raise_for_status()
        # Parse the response as JSON
        jsontxt = json.loads(html.text)
        # Get the new refresh token and access token
        refresh_token = jsontxt['refresh_token']
        access_token = jsontxt['access_token']
        # Get the public key
        public_key = get_public_key()
        # Encrypt the refresh token with the public key
        encrypted_token = encrypt_with_public_key(refresh_token, public_key)
        # Open the file in binary write mode
        with open(token_path, 'wb+') as f:
            # Clear the file content
            f.truncate(0)
            # Write the encrypted token
            f.write(encrypted_token)
    except (req.exceptions.HTTPError, json.decoder.JSONDecodeError) as e:
        # Print the error message if the request failed
        print("Error in requesting token:", e)
    except (ValueError, TypeError) as e:
        # Print the error message if the encryption failed
        print("Error in encrypting token:", e)

def main():
    # Open the file in binary read mode
    with open(token_path, "rb+") as fo:
        # Read the refresh token
        refresh_token = fo.read().decode()
    # Request a new token with the refresh token
    request_token(refresh_token)

main()
