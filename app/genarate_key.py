import configparser
import os
import secrets

def newSecretKey():
    ini_file_path = os.path.join('Bin','config.INI')
    config = configparser.ConfigParser()
    config.read(ini_file_path)
    config['SECRET']['SECRET_KEY'] = secrets.token_urlsafe(64)

    with open(ini_file_path, 'w') as configFile:
        config.write(configFile)

if __name__ == "__main__":
    newSecretKey()