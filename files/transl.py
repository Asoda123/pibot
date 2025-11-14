import json
import os

import user_storage as us

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "translations.json")


def load_info():
    with open(DATA_FILE, "r", encoding="utf-8") as data:
        return json.load(data)

def set_to_lang(option : str, uid : int ):
    info = load_info()
    return info.get(option, {}).get(us.get_user(uid)['lang'])