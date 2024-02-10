import requests
import sys
import rsa
import json

# Define file paths
PATH = sys.path[0] + '/temp.txt'
PUBLIC_KEY_PATH = sys.path[0] + '/public_key.txt'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'







def get_token(refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'redirect_uri': 'http://localhost:53682/'
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code == 200:
        jsontxt = response.json()
        new_refresh_token = jsontxt.get('refresh_token')
        if new_refresh_token:
            return new_refresh_token
        else:
            print("Error: Refresh token not found in response.")
            return None
    else:
        print(f"Error: Failed to get token - HTTP {response.status_code}")
        return None

def encrypt_token(token, public_key_path):
    with open(public_key_path, "rb") as key_file:
        try:
            public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
            encrypted_token = rsa.encrypt(token.encode(), public_key)
            return encrypted_token
        except (IOError, ValueError, rsa.pkcs1.CryptoError) as e:
            print(f"Error: Encryption failed - {e}")
            return None

def write_to_file(data, file_path):
    if data is not None and file_path is not None:
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
            print("Encrypted token has been written to:", file_path)
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
        encrypted_token = encrypt_token(new_refresh_token, PUBLIC_KEY_PATH)

        # Write the encrypted token to the file
        if encrypted_token:
            write_to_file(encrypted_token, PATH)

if __name__ == '__main__':
    main()
