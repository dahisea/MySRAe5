import requests
import sys
import rsa
import base64















# Register an Azure app first, ensure the app has the following permissions:
# files: Files.Read.All, Files.ReadWrite.All, Sites.Read.All, Sites.ReadWrite.All
# user: User.Read.All, User.ReadWrite.All, Directory.Read.All, Directory.ReadWrite.All
# mail: Mail.Read, Mail.ReadWrite, MailboxSettings.Read, MailboxSettings.ReadWrite
# After registration, be sure to click the button representing xxx to grant admin consent; otherwise, the Outlook API cannot be invoked.
PATH = sys.path[0] + '/temp.txt'
PUBLIC_KEY_PATH = sys.path[0] + '/public_key.txt'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

def get_token():
    # Read the refresh token from the file
    with open(PATH, 'r') as file:
        refresh_token = file.read()
    # Define the request header
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")).decode("utf-8")}'
    }
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    try:
        # Send a post request
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()  # Raise error for non-2xx responses
        # Parse the response result
        response_json = response.json()
        # Get the new refresh token
        refresh_token = response_json.get('refresh_token')
        # Write the new refresh token to the file
        with open(PATH, 'w+') as file:
            file.write(refresh_token)
        # Return the access token
        return response_json.get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {e}")
        return None
    except ValueError as e:
        print(f"Error: Response is not a valid JSON format - {e}")
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

def main():
    # Get the access token
    access_token = get_token()
    # Do not store the access token
    # Use the access token to access the Outlook API
    # ...
    # Get the refresh token from the file
    with open(PATH, 'r') as file:
        refresh_token = file.read()
    # Encrypt the refresh token
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        try:
            public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
            encrypted_token = encrypt_token(refresh_token, public_key)
        except IOError as e:
            print(f"Error: Failed to load public key - {e}")
    # Write the encrypted token to the file
    if encrypted_token:
        write_to_file(encrypted_token, PATH)

if __name__ == '__main__':
    main()
