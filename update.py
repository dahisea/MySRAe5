import requests as req
import json
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding










# Define the file path
path = sys.path[0] + '/temp.txt'

# RSA key paths
PUBLIC_KEY_PATH = "public_key.txt"
PRIVATE_KEY_PATH = "private_key.txt"

# Define the function to get the token
def get_token(encrypted_refresh_token):
    # Load private key
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    # Decrypt the refresh token
    decrypted_refresh_token = private_key.decrypt(
        encrypted_refresh_token,
        padding.PKCS1v15()
    )

    # Simulate getting new refresh token (in real scenario, this would come from the OAuth response)
    new_refresh_token = "new_refresh_token_example"

    # Load public key
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Encrypt the new refresh token
    encrypted_new_refresh_token = public_key.encrypt(
        new_refresh_token.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=padding.algorithms.MGF1.SHA1),
            algorithm=padding.OAEP.ALGORITHM.SHA1,
            label=None
        )
    )

    return encrypted_refresh_token, encrypted_new_refresh_token

# Define the main function
def main():
    # Read the encrypted refresh token from the file
    with open(path, "rb") as f:
        encrypted_refresh_token = f.read()

    # Get the new access token and encrypted new refresh token
    try:
        encrypted_refresh_token, encrypted_new_refresh_token = get_token(encrypted_refresh_token)
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Write the new encrypted refresh token to the file
    with open(path, "wb") as f:
        f.write(encrypted_new_refresh_token)

    print("New encrypted refresh token:", encrypted_new_refresh_token.hex())

# Execute the main function
main()
