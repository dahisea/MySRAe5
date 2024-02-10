import requests
import rsa

















# Define constants
TOKEN_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# Client ID and secret
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

def encrypt_data(data, public_key):
  return rsa.encrypt(data.encode(), public_key)

def decrypt_data(encrypted_data, private_key):
  return rsa.decrypt(encrypted_data, private_key).decode()

def get_token(refresh_token):
  # Request headers
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  # Request parameters
  data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': 'http://localhost:53682/'
  }
  try:
    # Send POST request
    response = requests.post(TOKEN_ENDPOINT, data=data, headers=headers)
    response.raise_for_status()  # Raise error for bad status codes
    # Parse response
    token_data = response.json()
    new_refresh_token = token_data['refresh_token']
    access_token = token_data['access_token']
    # Write new token to file
    with open('temp.txt', 'wb') as f:
      f.write(new_refresh_token.encode())
  except requests.RequestException as e:
    print(f"Error fetching token: {e}")

def read_private_key():
  try:
    # Read private key
    with open('private_key.txt', 'rb') as f:
      private_key_data = f.read()
    # Load private key
    private_key = rsa.PrivateKey.load_pkcs1(private_key_data)
    return private_key
  except FileNotFoundError as e:
    print(f"File not found: {e}")
  except rsa.DecryptionError as e:
    print(f"Error decrypting private key: {e}")

def decrypt_refresh_token(encrypted_token, private_key):
  try:
    # Decrypt refresh token
    decrypted_token = rsa.decrypt(encrypted_token, private_key).decode()
    return decrypted_token
  except rsa.DecryptionError as e:
    print(f"Error decrypting refresh token: {e}")

def main():
  # Read encrypted token
  with open('temp.txt', 'rb') as f:
    encrypted_token = f.read()
  # Decrypt refresh token
  private_key = read_private_key()
  decrypted_token = decrypt_refresh_token(encrypted_token, private_key)
  # Call function to get token
  get_token(decrypted_token)

# Execute main function
if __name__ == "__main__":
  main()
