import configparser
import os
from typing import Optional


class Settings:

    # __parent_dic = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    __ini_file_path = os.path.join('Bin', 'config.INI')

    __config = configparser.ConfigParser()
    __config.read(__ini_file_path)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    PROJECT_NAME: str = __config['BASIC']['PROJECT_NAME']
    API_URL: str = __config['BASIC']['api_base_url']
    WEB_URL: str = __config['BASIC']['web_base_url']

    DB_SCHEME: str = __config['DATABASE']['DB_SCHEME']
    DB_SERVER: str = __config['DATABASE']['DB_SERVER']
    DB_PORT: int = __config['DATABASE']['DB_PORT']
    DB_USER: str = __config['DATABASE']['DB_USER']
    DB_PASSWORD: str = __config['DATABASE']['DB_PASSWORD']
    DB_DATABASE: str = __config['DATABASE']['DB_DATABASE']
    DB_URL: str = __config['DATABASE']['DB_SCHEME']+'://'+__config['DATABASE']['DB_SERVER'] + \
        ':'+__config['DATABASE']['DB_PORT']+'/' + \
        __config['DATABASE']['DB_DATABASE']

    REDIS_HOST: str = __config['Redis']['REDIS_HOST']
    REDIS_PORT: int = __config['Redis']['REDIS_PORT']
    REDIS_URL: str = 'redis://'+__config['Redis']['REDIS_HOST']+':'+__config['Redis']['REDIS_PORT']+'/0'

    SECRET_KEY: str = __config['SECRET']['SECRET_KEY']

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = __config['MAIL']['mail_port']
    SMTP_HOST: Optional[str] = __config['MAIL']['mail_host']
    SMTP_USER: Optional[str] = __config['MAIL']['mail_user']
    SMTP_PASSWORD: Optional[str] = __config['MAIL']['mail_password']
    EMAILS_FROM_EMAIL: Optional[str] = __config['MAIL']['mail_from_address']
    EMAILS_FROM_NAME: Optional[str] = __config['MAIL']['mail_from_name']

    S3_BUCKET_NAME: str = __config['AWS']['bucket_name']
    AWS_REGION: str = __config['AWS']['region_name']
    AWS_ACCESS_KEY: str = __config['AWS']['aws_access_key_id']
    AWS_SECRET_KEY: str = __config['AWS']['aws_secret_access_key']


setting = Settings()
