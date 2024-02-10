import requests as req
import json
import sys
import base64  # Import for base64 encoding











path = sys.path[0] + '/temp.txt'

# Define the function to get the token
def get_token(base64_encoded_refresh_token):
    # Decode base64-encoded refresh token
    decoded_refresh_token = base64.b64decode(base64_encoded_refresh_token).decode('utf-8')

    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': decoded_refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }
    # Send a post request
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    jsontxt = json.loads(html.text)
    access_token = jsontxt['access_token']

    # Base64 encode the new refresh token
    new_refresh_token = jsontxt['refresh_token']
    base64_encoded_new_refresh_token = base64.b64encode(new_refresh_token.encode('utf-8')).decode('utf-8')

    return access_token, base64_encoded_new_refresh_token

# Define the main function
def main():
    # Read the base64-encoded refresh token from the file
    with open(path, "rb") as f:
        base64_encoded_refresh_token = f.read().decode('utf-8')

    # Get the new access token and base64-encoded new refresh token
    try:
        access_token, base64_encoded_new_refresh_token = get_token(base64_encoded_refresh_token)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Write the new base64-encoded refresh token to the file
    with open(path, "wb") as f:
        f.write(base64_encoded_new_refresh_token.encode('utf-8'))

# Execute the main function
main()
