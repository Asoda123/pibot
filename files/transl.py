import json
from pathlib import Path
import user_storage as us
DATA_FILE = Path('translations.json')


def load_info():
    with open(DATA_FILE,'r', encoding='utf-8') as data:
        return json.load(data)

def set_to_lang(option : str, uid : int ):
    info = load_info()
    return info.get(option, {}).get(us.get_user(uid)['lang'])