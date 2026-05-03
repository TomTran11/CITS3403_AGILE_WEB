import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LANG_PATH = os.path.join(BASE_DIR, 'data', 'languages.json')

with open(LANG_PATH) as f:
    LANGUAGE_DATA = set(json.load(f).values())