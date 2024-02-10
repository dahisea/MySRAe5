import requests as req
import json
import sys
import time
import rsa











# Define the file path
path = sys.path[0] + r'/temp.txt'

# RSA key paths
PUBLIC_KEY_PATH = "public_key.pem"
PRIVATE_KEY_PATH = "private_key.pem"

# Define the function to get the token
def get_token(encrypted_refresh_token):
    # Decrypt the refresh token
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    refresh_token = rsa.decrypt(encrypted_refresh_token, private_key)

    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token.decode('utf-8'),
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }
    # Send a post request
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    jsontxt = json.loads(html.text)
    # Get the new token
    new_refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']

    # Encrypt the new refresh token
    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    encrypted_refresh_token = rsa.encrypt(new_refresh_token.encode('utf-8'), public_key)

    return encrypted_refresh_token, access_token

# Define the main function
def main():
    # Read the encrypted refresh token from the file
    with open(path, "rb") as f:
        encrypted_refresh_token = f.read()

    # Get the new access token and refresh token
    encrypted_refresh_token, access_token = get_token(encrypted_refresh_token)

    # Write the new encrypted refresh token to the file
    with open(path, "wb") as f:
        f.write(encrypted_refresh_token)

# Execute the main function
main()
