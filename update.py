import requests as req
import json
import sys
import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes

# Define the file paths
public_key_path = sys.path[0] + r'/public_key.pem'
token_path = sys.path[0] + r'/temp.txt'

def load_public_key():
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def encrypt_token(token, public_key):
    token = base64.b64encode(token.encode()) # Encode the token to base64
    cipher_text = public_key.encrypt(
        token,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text

def gettoken(refresh_token):
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': id,
            'client_secret': secret,
            'redirect_uri': 'http://localhost:53682/'
        }
        html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
        html.raise_for_status() # Raise an exception if the status code is not 200
        jsontxt = json.loads(html.text)
        refresh_token = jsontxt['refresh_token']
        access_token = jsontxt['access_token']
        public_key = load_public_key()
        encrypted_token = encrypt_token(refresh_token, public_key)
        with open(token_path, 'wb+') as f: # Open the file in binary write mode
            f.truncate(0) # Clear the file content
            f.write(encrypted_token) # Write the encrypted token
    except (req.exceptions.HTTPError, json.decoder.JSONDecodeError) as e:
        print("Error in requesting token:", e)
    except (ValueError, TypeError) as e:
        print("Error in encrypting token:", e)

def main():
    with open(token_path, "rb+") as fo: # Open the file in binary read mode
        refresh_token = fo.read().decode() # Read the token
    gettoken(refresh_token)

main()
