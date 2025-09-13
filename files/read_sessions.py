import json
import random
from pathlib import Path
from humanfriendly.terminal import message
from pyexpat.errors import messages

import user_storage as us
from random import randint
DATA_FILE = Path('sessions.json')
teacher_is_found = False

def load_info():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE,'r', encoding='utf-8') as data:
        return json.load(data)

def save_info(users : dict):
    with open(DATA_FILE, 'w') as data:
        json.dump(users,data,indent=2)

def create_a_queue(user_id=None,teacher_id=None):
    sessions = load_info()
    sessions[str(random.randint(10000,99999))]= {"student" : {'id' : user_id,     'messages' : []},
                                                       "teacher" : {'id' : teacher_id,  'messages' : []}}
    save_info(sessions)

def check_whether_queue_is_full(uid):
    sessions = load_info()
    uid = str(uid)
    for id_ in sessions.keys():
        if uid in sessions.get(id_).get('student').get('id') and sessions.get(id_).get('teacher').get('id') is not None or uid in sessions.get(id_).get('teacher').get('id') and  sessions.get(id_).get('student').get('id') is not None:
            return True
        else: pass
    else:
        return False

def find_session_id(uid):
    sessions = load_info()
    uid = str(uid)
    for id_ in sessions.keys():
        if uid in sessions.get(id_).get('student').get('id') or uid in sessions.get(id_).get('teacher').get('id'):
            return id_
        else: pass

def find_opponent_id(uid):
    sessions = load_info()
    uid = str(uid)
    for session_id, session_data in sessions.items():
        if session_data['student']['id'] == uid:
            return int(session_data['teacher']['id'])
        if session_data['teacher']['id'] == uid:
            return int(session_data['student']['id'])
    return None

def find_student_id(uid):
    sessions = load_info()
    uid = str(uid)
    for session_id, session_data in sessions.items():
        if session_data['student']['id'] == uid or session_data['teacher']['id'] == uid:
            return session_data['student']['id']
    return None


def teacher_to_true():
    global teacher_is_found
    teacher_is_found = True



def add_user_to_queue(uid : int):
    sessions = load_info()
    new_chat_id = ''
    uid = str(uid)
    if len(sessions) == 0:
        create_a_queue(user_id=uid)
    else:
        for id_ in sessions.keys():
            # print(sessions.get(id_).get('student').get('id'))
            if sessions.get(id_).get('student').get('id') is not None:
                pass
            if sessions.get(id_).get('student').get('id') == uid:
                break
            else:
                create_a_queue(user_id=uid)
                for ids in sessions.keys():
                    if sessions.get(ids).get('student').get('id') == uid:
                        new_chat_id = ids
                sessions[new_chat_id]['student']['id'] = uid
                save_info(sessions)
                break


def add_teacher_queue(uid : int):
    sessions = load_info()

    uid = str(uid)
    if len(sessions) == 0:
        return False
    else:
        for id_ in sessions.keys():
            print(sessions.get(id_).get('teacher').get('id'))
            if sessions.get(id_).get('teacher').get('id') is not None:
                continue
            elif sessions.get(id_).get('teacher').get('id') == uid:
                return False
            else:
                sessions[id_]['teacher']['id'] = uid
                save_info(sessions)
                return True

def del_session(uid : int):
    uid = str(uid)
    sess_id = find_session_id(uid)
    sessions = load_info()
    sessions.pop(sess_id)
    save_info(sessions)


def add_message(message: str,uid : int, teacher=False,user=False):
    sessions = load_info()
    print(sessions)
    uid = str(uid)
    session_id = find_session_id(uid)

    for key, value in sessions[session_id].items():
        # print("value : ",value)
        for inner_keys, inner_values in value.items():
            # print("inner_values : ",inner_values, 'inner_key : ',inner_keys)
            if inner_values == uid:
                sessions[session_id][key]['messages'].append(message)
                save_info(sessions)

def get_last_message(uid : int):
    sessions = load_info()
    uid = str(uid)
    session_id = find_session_id(uid)
    session = sessions[session_id]
    for role, user_data in session.items():
        if isinstance(user_data, dict) and user_data.get('id') == uid:
            messages = user_data.get('messages')
            if messages:
                return messages[-1]




