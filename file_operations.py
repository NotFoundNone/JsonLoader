import json
import os
from db_config import DATA_DIR

def load_json(date):
    filename = f'{DATA_DIR}/data_{date.strftime("%Y-%m-%d")}.json'
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)