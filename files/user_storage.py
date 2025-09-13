import json
from pathlib import Path

DATA_FILE = Path('data.json')

if not DATA_FILE.exists():
    DATA_FILE.write_text('{}')

def load_users():
    with open(DATA_FILE,'r') as data:
        return json.load(data)

def save_users(users : dict):
    with open(DATA_FILE, 'w') as data:
        json.dump(users,data,indent=2)

def add_user(user_id : int, eqs : list, username : str, lang='en', role='user'):
    users = load_users()
    users[str(user_id)] = {'username' : username,'eqs' : eqs,'lang': lang, 'role' : role}
    save_users(users)

def get_user(user_id : int):
    users = load_users()
    return users.get(str(user_id))

def add_or_update_info(user_id : int, username : str = None, eqs : list = None, lang : str = None, role : str = None):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        users[uid] = {}

    if eqs is not None:
        users[uid]['eqs'] = eqs

    if lang is not None:
        users[uid]['lang'] = lang

    if username is not None:
        users[uid]['username'] = username

    if role is not None:
        users[uid]['role'] = role

    save_users(users)

