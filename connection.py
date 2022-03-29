# pip3 install mysql-connector-python
# pip3 install python-decouple
# pip3 install flask

import mysql.connector as mysql
import os
from decouple import Config, RepositoryEnv

DOTENV_FILE = os.path.abspath('./.env')
env_config = Config(RepositoryEnv(DOTENV_FILE))

connection = mysql.connect(
            host=env_config.get('DB_HOST', default='localhost'),
            port=env_config.get("DB_PORT", default=3306),
            user=env_config.get('DB_USER'),
            password=env_config.get('DB_PASSWORD'),
            database=env_config.get('DB_NAME'),
            buffered=True
        )

cursor = connection.cursor()


