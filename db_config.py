import os
from dotenv import load_dotenv

# Путь к local.env файлу
env_path = os.path.join(os.path.dirname(__file__), 'local.env')

# Загрузка переменных окружения из local.env файла
load_dotenv(dotenv_path=env_path)

DB_NAME = os.getenv('DB_NAME', 'testPython2')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DATA_DIR = os.getenv('DATA_DIR', 'data')