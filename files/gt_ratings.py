import json
from pathlib import Path
import read_sessions as rs

DATA_FILE = Path('ratings.json')

def load_info():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE,'r', encoding='utf-8') as data:
        return json.load(data)

def save_info(users : dict):
    with open(DATA_FILE, 'w') as data:
        json.dump(users,data,indent=2)

def create_a_rating(uid, rating):
    uid = str(uid)
    rating = int(rating)
    teachers_id = rs.find_opponent_id(uid)
    add_or_update_info(teachers_id,rating)

def get_rating(uid):
    uid = str(uid)
    ratings = load_info()
    t_ratings = ratings.get(uid)
    if t_ratings:
        return str(round((sum(t_ratings)/len(t_ratings)),1))
    return '0'


def add_or_update_info(user_id : str, rating: int = None):
    users = load_info()
    uid = str(user_id)
    if uid not in users:
        users[uid] = []

    if rating != None:
        users[uid].append(rating)


    save_info(users)