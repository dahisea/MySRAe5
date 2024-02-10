import requests
import json
import sys














# Define constants
TOKEN_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# File path
path = sys.path[0] + r'/temp.txt'

# Define function to get token
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
        with open(path, 'w+') as f:
            f.write(new_refresh_token)
    except requests.RequestException as e:
        print("Error fetching token:", e)

# Main function
def main():
    try:
        # Read refresh token from file
        with open(path, "r+") as f:
            refresh_token = f.read()
        # Call function to get token
        get_token(refresh_token)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")

# Execute main function
if __name__ == "__main__":
    main()
