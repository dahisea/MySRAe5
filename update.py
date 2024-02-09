# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import rsa














# Define the file path
path = sys.path[0] + r'/temp.txt'
# Define the public key file path
public_key_path = sys.path[0] + r'/public_key.txt'
# Get the id and secret from elsewhere

# Define the function to get the token
def gettoken(id, secret):
    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'client_credentials',
        'client_id': id,
        'client_secret': secret,
        'scope': 'https://management.azure.com/.default'
    }
    # Send a post request
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    jsontxt = json.loads(html.text)
    # Get the token
    token = jsontxt['access_token']
    # Write the token to the file
    with open(path, 'w+') as f:
        f.write(token)
    # Return the token
    return token

# Define the function to encrypt the token
def encrypt(token):
    # Load the public key from the file
    with open(public_key_path, 'rb') as f:
        publickey = rsa.PublicKey.load_pkcs1(f.read())
    # Encrypt the token using the public key
    ciphertext = rsa.encrypt(token.encode(), publickey)
    # Return the ciphertext
    return ciphertext

# Define the main function
def main():
    # Call the function to get the token
    token = gettoken(id, secret)
    # Call the function to encrypt the token
    ciphertext = encrypt(token)
    # Print the ciphertext
    print(ciphertext)

# Execute the main function
main()
