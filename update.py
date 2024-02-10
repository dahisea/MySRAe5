# Import the required modules
import requests
import sys
import rsa
import base64












# Define the constants
PATH = sys.path[0] + '/temp.txt'
PUBLIC_KEY_PATH = sys.path[0] + '/public_key.txt'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
SCOPE = 'https://graph.microsoft.com/.default'

def get_token():
    """Get and return the access token and the refresh token from Microsoft OAuth2.0 service."""
    # Define the request header and parameters
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # Use base64.b64encode to encode the client ID and secret to base64
        'Authorization': f'Basic {base64.b64encode((CLIENT_ID + ":" + CLIENT_SECRET).encode("utf-8")).decode("utf-8")}'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': SCOPE
    }
    # Send a post request and get the response
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    # Parse the response as JSON
    try:
        response_json = response.json()
    except ValueError: # Handle the JSON decoding error
        print("Error: Response is not a valid JSON format.")
        return None, None
    # Check if the response contains an access token and a refresh token
    if 'access_token' in response_json and 'refresh_token' in response_json:
        access_token = response_json['access_token']
        refresh_token = response_json['refresh_token']
        print(f"Access token: {access_token}") # Print the access token
        print(f"Refresh token: {refresh_token}") # Print the refresh token
        return access_token, refresh_token # Return the tokens
    else:
        print("Error: Token not found in response.")
        return None, None

def encrypt_token(token, public_key):
    """Encrypt the token using RSA public key and return the encrypted token."""
    # Check if the token and the public key are not None
    if token is not None and public_key is not None:
        # Use rsa.encrypt to encrypt the token
        encrypted_token = rsa.encrypt(token.encode(), public_key)
        return encrypted_token # Return the encrypted token
    else:
        print("Error: Token or public key is None.")
        return None

def write_to_file(data, file_path):
    """Write the data to the file in binary mode."""
    # Check if the data and the file path are not None
    if data is not None and file_path is not None:
        # Use with statement to automatically close the file
        with open(file_path, 'wb') as file:
            file.write(data) # Write the data to the file
    else:
        print("Error: Data or file path is None.")

def main():
    """The main function of the program."""
    # Get the tokens
    access_token, refresh_token = get_token()
    # Load the public key
    with open(PUBLIC_KEY_PATH, "rb") as key_file: # Use with statement to automatically close the file
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
    # Encrypt the refresh token
    encrypted_token = encrypt_token(refresh_token, public_key)
    # Write the encrypted token to the file
    write_to_file(encrypted_token, PATH)

# Execute the main function
if __name__ == '__main__':
    main()
