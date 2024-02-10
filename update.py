import requests as req
import sys
import rsa







# Define the file paths
path = sys.path[0] + '/temp.txt'
public_key_path = sys.path[0] + '/public_key.txt'


# Define the function to get the token
def gettoken():
    # Define the request header
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {(id + ":" + secret).encode("base64")}' # Use f-string to format the header
    }
    # Define the request parameters
    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }
    # Send a post request
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    try:
        jsontxt = html.json()
    except ValueError: # Handle the JSON decoding error
        print("Error: Response is not a valid JSON format.")
        return
    # Check if the response contains an access token and a refresh token
    if 'access_token' in jsontxt and 'refresh_token' in jsontxt:
        access_token = jsontxt['access_token']
        refresh_token = jsontxt['refresh_token']
        print(f"Access token: {access_token}") # Print the access token
        print(f"Refresh token: {refresh_token}") # Print the refresh token
        return refresh_token # Return the refresh token
    else:
        print("Error: Token not found in response.")
        return

# Define the main function
def main():
    # Call the function to get the token
    refresh_token = gettoken()
    # Check if the refresh token is not None
    if refresh_token is not None:
        # RSA encrypt the refresh token
        with open(public_key_path, "rb") as key_file: # Use with statement to automatically close the file
            public_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_file.read())
            encrypted_token = rsa.encrypt(refresh_token.encode(), public_key)
        # Write the encrypted token to the file
        with open(path, 'wb') as f:
            f.write(encrypted_token)

# Execute the main function
main()
