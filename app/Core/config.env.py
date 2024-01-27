import os
from dotenv import load_dotenv
from typing import Optional

# Navigate up one directory to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file in the project root
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

class Settings:

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    API_URL: str = os.getenv('API_URL')
    WEB_URL: str = os.getenv('WEB_URL')

    DB_SCHEME: str = os.getenv('DB_SCHEME')
    DB_SERVER: str = os.getenv('DB_SERVER')
    DB_PORT: int = int(os.getenv('DB_PORT'))
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_DATABASE: str = os.getenv('DB_DATABASE')
    DB_URL: str = os.getenv('DB_SCHEME') + '://' + os.getenv('DB_SERVER') + \
        ':' + str(os.getenv('DB_PORT')) + '/' + os.getenv('DB_DATABASE')

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT'))
    REDIS_URL: str = 'redis://' + os.getenv('REDIS_HOST') + ':' + \
        str(os.getenv('REDIS_PORT')) + '/0'

    SECRET_KEY: str = os.getenv('SECRET_KEY')

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = int(os.getenv('SMTP_PORT'))
    SMTP_HOST: Optional[str] = os.getenv('SMTP_HOST')
    SMTP_USER: Optional[str] = os.getenv('SMTP_USER')
    SMTP_PASSWORD: Optional[str] = os.getenv('SMTP_PASSWORD')
    EMAILS_FROM_EMAIL: Optional[str] = os.getenv('EMAILS_FROM_EMAIL')
    EMAILS_FROM_NAME: Optional[str] = os.getenv('EMAILS_FROM_NAME')

    S3_BUCKET_NAME: str = os.getenv('S3_BUCKET_NAME')
    AWS_REGION: str = os.getenv('AWS_REGION')
    AWS_ACCESS_KEY: str = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY: str = os.getenv('AWS_SECRET_KEY')


setting = Settings()
