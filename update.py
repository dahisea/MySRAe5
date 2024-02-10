# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import time










# Register an Azure app first, ensure the app has the following permissions:
# files: Files.Read.All, Files.ReadWrite.All, Sites.Read.All, Sites.ReadWrite.All
# user: User.Read.All, User.ReadWrite.All, Directory.Read.All, Directory.ReadWrite.All
# mail: Mail.Read, Mail.ReadWrite, MailboxSettings.Read, MailboxSettings.ReadWrite
# After registration, be sure to click the button representing xxx to grant admin consent; otherwise, the Outlook API cannot be invoked.

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
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    # Parse the response result
    jsontxt = json.loads(html.text)
    # Get the new token
    refresh_token = jsontxt['refresh_token']
    # Write the new token to the file
    with open(path, 'wb') as f:
    f.write(refresh_token.encode('utf-8'))


# Define the main function
def main():
    # Open the file
    with open(path, "rb") as fo:
        # Read the file content
        refresh_token = fo.read()
    # Call the function to get the token
    get_token(refresh_token)

# Execute the main function
main()
