# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import time

# Define the file path
path = sys.path[0] + r'/temp.txt'








# Define the function to get the token
def get_token(refresh_token):
    # Define the request header
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # Define the request parameters
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }
    # Send a post request
    response = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    if response.status_code == 200:
        jsontxt = response.json()
        new_refresh_token = jsontxt.get('refresh_token')
        if new_refresh_token:
            # Write the new token to the file
            with open(path, 'w+') as f:
                f.write(new_refresh_token)
        else:
            print("Error: Refresh token not found in response.")
    else:
        print(f"Error: Failed to get token - HTTP {response.status_code}")

# Define the main function
def main():
    # Open the file
    with open(path, "r") as fo:
        # Read the file content
        refresh_token = fo.read().strip()
    # Call the function to get the token
    get_token(refresh_token)

# Execute the main function
if __name__ == "__main__":
    main()
