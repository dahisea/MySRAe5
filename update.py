import requests as req
import json
import sys
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa










# Define the file path
path = sys.path[0] + r'/temp.txt'

# RSA key paths
PUBLIC_KEY_PATH = "public_key.txt"
PRIVATE_KEY_PATH = "private_key.txt"

# Define the function to get the token
def get_token(encrypted_refresh_token):
    # Load private key
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    # Decrypt the refresh token
    decrypted_refresh_token = private_key.decrypt(
    encrypted_refresh_token,
    padding.PKCS1v15()
)


    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': decrypted_refresh_token.decode('utf-8'),
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

    # Encrypt the new refresh token (optional, using cryptography)
    # ... (add implementation if needed)

    return encrypted_refresh_token, access_token

# Define the main function
def main():
    # Read the encrypted refresh token from the file
    with open(path, "rb") as f:
        encrypted_refresh_token = f.read()

    # Get the new access token and refresh token
    try:
        encrypted_refresh_token, access_token = get_token(encrypted_refresh_token)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Write the new encrypted refresh token to the file (optional)
    # ... (add implementation if needed)

    print("Access token:", access_token)

# Execute the main function
main()
