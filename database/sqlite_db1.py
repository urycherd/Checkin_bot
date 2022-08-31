from dataclasses import field
import time
import sqlite3 as sq
import os

PATH_TO_DB = os.path.join('database','checkin_bot_db.db')


def sql_start():
    base = sq.connect(PATH_TO_DB)
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute("""CREATE TABLE IF NOT EXISTS event(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    type TEXT NOT NULL, 
                    user_id INT NOT NULL, 
                    title TEXT NOT NULL, 
                    description TEXT, 
                    seats_number INT, 
                    publication_date INT DEFAULT NULL, 
                    data_start TEXT INT NULL, 
                    data_end TEXT INT NULL ); """)
    base.commit()
    base.execute("""CREATE TABLE IF NOT EXISTS feedback(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    user_id INT NOT NULL, 
                    event_id INT NOT NULL, 
                    grade INT NOT NULL, 
                    review TEXT, 
                    time INT);""")
    base.commit()
    base.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY NOT NULL, 
                    login TEXT Unique NOT NULL, 
                    campus TEXT NOT NULL, 
                    type TEXT DEFAULT user, 
                    time INT);""")
    base.commit()
    base.execute("""CREATE TABLE IF NOT EXISTS registration(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    user_id INT NOT NULL, 
                    event_id INT NOT NULL, 
                    registration_time INT NOT NULL);""")
    base.commit()
    base.execute("""CREATE TABLE IF NOT EXISTS checkins(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    user_id INT NOT NULL, 
                    event_id INT NOT NULL, 
                    time INT NOT NULL);""")
    base.commit()
    base.close()


def select_db(table, fields, condition=None):
    base = sq.connect(PATH_TO_DB)
    cur = base.cursor()
    if (condition is None):
        req = f"SELECT {','.join(fields)} FROM {table}"
    else:
        req = f"SELECT {','.join(fields)} FROM {table} WHERE {condition}"
    cur.execute(req)
    select = cur.fetchall()
    base.close()
    return select


# Insert не обрабатывает ошибку когда подаётся пользователь, который уже есть
# то есть не уникальную переменную пытаются записать
def insert_db(table, fields, parameters):
    base = sq.connect(PATH_TO_DB)
    cur = base.cursor()
    quest = ['?'] * len(parameters)
    req = f"INSERT INTO {table}({','.join(fields)}) VALUES({','.join(quest)})"
    cur.execute(req, parameters)
    base.commit()
    base.close()


# update_db("users", "login", "mikabuto2", "login = 'mikabuto'")
# Также, надо просто в кавычки. Перенёс value в запрос
def update_db(table, field, value, condition):
    base = sq.connect(PATH_TO_DB)
    cur = base.cursor()
    print(condition)
    req = f"UPDATE {table} SET {field} = '{value}' WHERE {condition}"
    cur.execute(req)
    base.commit()
    base.close()


#delete_db('users', 'login = "grishe4ka2"')
def delete_db(table, condition):
    base = sq.connect(PATH_TO_DB)
    cur = base.cursor()
    req = f"DELETE FROM {table} WHERE {condition}"
    cur.execute(req)
    base.commit()
    base.close()


sql_start()
