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
CLIENT_ID = 'your_client_id' # Replace with your actual client ID
CLIENT_SECRET = 'your_client_secret' # Replace with your actual client secret
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
SCOPE = 'https://graph.microsoft.com/.default' # Replace with your desired scope

def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")).decode("utf-8")}'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': SCOPE
    }
    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()  # Raise error for non-2xx responses
        response_json = response.json()
        access_token = response_json.get('access_token')
        refresh_token = response_json.get('refresh_token')
        if access_token and refresh_token:
            print(f"Access token: {access_token}")
            print(f"Refresh token: {refresh_token}")
            return access_token, refresh_token
        else:
            print("Error: Token not found in response.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed - {e}")
        return None, None
    except ValueError as e:
        print(f"Error: Response is not a valid JSON format - {e}")
        return None, None

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
    access_token, refresh_token = get_token()
    if access_token and refresh_token:
        with open(PUBLIC_KEY_PATH, "rb") as key_file:
            try:
                public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
                encrypted_token = encrypt_token(refresh_token, public_key)
                if encrypted_token:
                    write_to_file(encrypted_token, PATH)
            except IOError as e:
                print(f"Error: Failed to load public key - {e}")

if __name__ == '__main__':
    main()
