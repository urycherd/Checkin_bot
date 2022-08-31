from cmath import log
from database.sqlite_db1 import *

import time


def is_admin(user_id):
    type_user = select_db("users", ["type"], f"id == '{user_id}'")
    return type_user[0][0] == 'admin'


def get_login(user_id):
    login = select_db('users', ['login'], f'id={user_id}')
    return login[0][0]


def get_future_user_events(user_id):
    event_ids = select_db('registration', ['event_id'], f'user_id={user_id}')
    array_events_id = [str(event_id[0]) for event_id in event_ids]
    events_info = select_db('event',
                           ['type', 'title', 'description', 'seats_number', 'publication_date', 'data_start', 'data_end', 'id'],
                           f"id in ({','.join(array_events_id)}) AND data_end > '{round(time.time())}' ORDER BY data_start DESC")
    return events_info


def get_past_user_events(user_id):
    event_ids = select_db("checkins", ["event_id"], f"user_id == '{user_id}'")
    strevent_ids = [str(event_id[0]) for event_id in event_ids]
    return select_db("event", ['type', 'title', 'description', 'seats_number', 'publication_date', 'data_start', 'data_end', 'id'], 
                    f"id in ({','.join(strevent_ids)}) ORDER BY data_start DESC")


def leave_feedback(user_id, event_id, grade, review):
    try:
        insert_db("feedback", ["user_id", "event_id", "grade", "review", "time"], [user_id, event_id, grade, review, round(time.time())])
        return True
    except Exception:
        return False


# функция записывает в БД отзыв про прошедшее событие с айдишником event_id в бд, на котором был зачекинен юзер с телеграмным user_id. Остальные два параметра про отзыв:
# eval - int от 0 до 5 (оценка мероприятия юзером по 5тибалльной шкале)
# message - string (строка с непосредственно отзывом)

# возвращает false в случае ошибки, true - в случае когда всё гуд
def user_checkined(user_id, event_id):
    try:
        insert_db('checkins', ['user_id', 'event_id', 'time'], [user_id, event_id, round(time.time())])
        return True
    except Exception:
        return False
# отметить у юзера с user_id, что он зачекинился на мероприятии с event_id

# возвращает false в случае ошибки, true - в случае когда всё гуд


def register_user(user_id, event_id):
    try:
        insert_db('registration', ['user_id', 'event_id', 'registration_time'], [user_id, event_id, round(time.time())])
        return True
    except Exception:
        return False
# отметить у юзера с user_id, что он зарегался на мероприятии с event_id

# возвращает false в случае ошибки, true - в случае когда всё гуд


def unregister_user (user_id, event_id):
    try:
        delete_db('registration', f'user_id={user_id} and event_id={event_id}')
        return True
    except Exception:
        return False


# отметить у юзера с user_id, что он отменил регистрацию на мероприятии с event_id

# возвращает false в случае ошибки, true - в случае когда всё гуд
def get_relevant_events(user_id):
    campus = get_user_campus(user_id)
    events = select_db("event",
                       ['type', 'title', 'description', 'seats_number', 'publication_date', 'data_start', 'data_end', 'id'],
                       f"type in ('Online', '{campus}') and data_end > {round(time.time())} ORDER BY data_start DESC")
    return events

# возвращает нечно массивоподобное со всей инфой про мероприятия, которые онлайн или по месту проведения совпадают с кампусам юзера с user_id


def get_my_organized_events(user_id):
    events = select_db("event",
                       ['type', 'title', 'description', 'seats_number', 'publication_date', 'data_start', 'data_end', 'id'],
                       f"user_id = {user_id}")
    return events


# возвращает нечто массивоподобное со списком всех мероприятий, организованных данным юзером user_id

def get_register_list(event_id):
    user_ids = select_db('registration', ['user_id'], f'event_id ={event_id}')
    struser_ids = [str(user_id[0]) for user_id in user_ids]
    register_list = select_db("users",
                           ["login"],
                           f"id IN ({','.join(struser_ids)})")
    return register_list

# возвращает список интровских/сберплатформовских логинов юзеров, зарегистрированных на event_id


def get_checkin_list(event_id):
    user_ids = select_db('checkins', ['user_id'], f'event_id ={event_id}')
    struser_ids = [str(user_id[0]) for user_id in user_ids]
    checkin_list = select_db("users",
                              ["login"],
                              f"id IN ({','.join(struser_ids)})")
    return checkin_list

# возвращает список интровских/сберплатформовских логинов юзеров, зачекиненых на event_id

# ❗️супер важно❗️везде user_id - это телеграмный айдишник, поэтому у юзера должно быть поле с теграмным айдишником, если вдруг его не было


def if_user_id_exist(user_id):
    name = select_db("users", ["login"], f"id == '{user_id}'")
    return len(name)


def if_user_login_exist(login):
    name = select_db("users", ["login"], f"login == '{login}'")
    return len(name)


def assign_admin(login):
    if if_user_login_exist(login):
        user_id = select_db("users", ["id"], f"login == '{login}'")[0][0]
        if not is_admin(user_id):
            update_db("users", "type", "admin", f"id == '{user_id}'")
            if is_admin(user_id):
                return True
    return False


def if_user_registered(user_id, event_id):
    user_registred = select_db("registration",
                    ['user_id'],
                    f'user_id = {user_id} AND event_id = {event_id}')
    if user_registred:
        return True
    return False


# возвращает true, если пользователь с user_id зареган на мероприятие с event_id

def if_user_checkined(user_id, event_id):
    user_checkined = select_db("checkins",
                    ['user_id'],
                    f'user_id = {user_id} AND event_id = {event_id}')
    if user_checkined:
        return True
    return False


# возвращает true, если пользователь с user_id чекинился на мероприятие с event_id

def get_user_campus(user_id):
    campus = select_db("users",
                       ['campus'],
                       f'id = "{user_id}"')
    return campus[0][0]
# возвращает кампус, в котором учится юзер с user_id
# нужна функция для записи в бд нового пользователя (но тут нужно обсудить, какие нам данные тебе выдавать)


def addnewuser(id, login, campus):
    try:
        insert_db('users', ['id', 'login', 'campus', 'time'], [id, login, campus, round(time.time())])
        return True
    except Exception:
        return False


def addnewevent(type, user_id, title, seats_number, data_start, data_end, description="", publication_date=None):
    try:
        insert_db('event', ['user_id', 'type', 'title', 'description', 'seats_number', 'publication_date', 'data_start', 'data_end'], \
        [user_id, type, title, description, seats_number, publication_date, data_start, data_end])
        return True
    except Exception:
        return False


def zero_admin(id, login, campus):
    addnewuser(id, login, campus)
    assign_admin(login)


def registed_users(event_id):
    return select_db("registration", ["COUNT(user_id)"], f"event_id == '{event_id}'")[0][0]


def if_left_feedback(user_id, event_id):
    res = select_db('feedback', ['*'], f'user_id={user_id} and event_id={event_id}')
    return len(res)


zero_admin(171036999, 'mika', 'MSK')
