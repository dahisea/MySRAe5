import requests
import sys
import rsa
import json













# Define file paths
PATH = sys.path[0] + '/temp.txt'
PUBLIC_KEY_PATH = sys.path[0] + '/public_key.txt'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

def gettoken(refresh_token):
    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }
    # Send a post request
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response result
        jsontxt = response.json()
        # Get the new token
        new_refresh_token = jsontxt.get('refresh_token')
        if new_refresh_token:
            # Write the new token to the file
            with open(PATH, 'w+') as f:
                f.write(new_refresh_token)
            return new_refresh_token
        else:
            print("Error: Refresh token not found in response.")
            return None
    else:
        print(f"Error: Failed to get token - HTTP {response.status_code}")
        return None

def encrypt_token(token, public_key):
    if token is not None and public_key is not None:
        try:
            encrypted_token = rsa.encrypt(token.encode(), public_key)
            return encrypted_token
        except rsa.pkcs1.CryptoError as e:
            print(f"Error: Encryption failed - {e}")
            return None
    else:
        print("Error: Token or public key is None.")
        return None

def write_to_file(data, file_path):
    if data is not None and file_path is not None:
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
        except IOError as e:
            print(f"Error: Failed to write to file - {e}")
    else:
        print("Error: Data or file path is None.")

def main():
    # Get the access token
    with open(PATH, 'rb') as file:
        refresh_token = file.read().strip()  # Strip any leading/trailing whitespaces
    new_refresh_token = get_token(refresh_token)
    
    if new_refresh_token:
        # Encrypt the new refresh token
        with open(PUBLIC_KEY_PATH, "rb") as key_file:
            try:
                public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
                encrypted_token = encrypt_token(new_refresh_token.encode(), public_key)
            except IOError as e:
                print(f"Error: Failed to load public key - {e}")
                return

        # Write the encrypted token to the file
        if encrypted_token:
            write_to_file(encrypted_token, PATH)

if __name__ == '__main__':
    main()
