import os
import secrets
from dotenv import load_dotenv

def newSecretKey():
    # Load environment variables from .env file in the project root
    load_dotenv()

    # Set the new secret key
    new_secret_key = secrets.token_urlsafe(64)
    os.environ['SECRET_KEY'] = new_secret_key

    # Optionally, update the .env file with the new secret key
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(dotenv_path, 'a') as dotenv_file:
        dotenv_file.write(f'\nSECRET_KEY={new_secret_key}')

if __name__ == "__main__":
    newSecretKey()
