from urllib import request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types
from create_bot import dp, bot
import database.functions as db
import utils.utils as ut
import time as ttime

b1 = KeyboardButton("Все мероприятия")
b2 = KeyboardButton("Моё расписание")
b3 = KeyboardButton("Прошедшие события")

base_kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
base_kb_client.add(b1).add(b2).add(b3)


b4 = KeyboardButton("MSK")
b5 = KeyboardButton("KAZ")
b6 = KeyboardButton("NSK")

kb_campus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
kb_campus.add(b4).add(b5).add(b6)

kb_numbers = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
kb_numbers.insert(KeyboardButton("0")).insert(KeyboardButton("1")).insert(KeyboardButton("2")).insert(KeyboardButton("3")).insert(KeyboardButton("4")).insert(KeyboardButton("5"))



# =========================Inline buttons=========================================

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text


# Ищет в массиве мероприятий мероприятие с event_id

def search_event(id_, event_id: int, time='future'):
	print(id_, event_id)
	if time == 'future':
		events = db.get_relevant_events(id_)
	elif time =='past':
		events = db.get_past_user_events(id_)
	print(events)
	for event in events:
		if event[-1] == event_id:
			return event
	return None


# Создаёт сообщение с описанием мероприятия

def create_event_description_message(event):
	res = f"""
	<b>Название мероприятия: </b> {event[1]}

	<b>Описание: </b>{event[2]}

	<b>Место проведения: </b>{event[0]}

	<b>Дата начала: </b>{ut.unix_to_time(event[5])}
	<b>Дата окончания: </b>{ut.unix_to_time(event[6])}

	<b>Количество мест: </b> {str(db.registed_users(event[-1]))}/{event[3]}"""
	return res

# Создание клавиатуры с нужным списком событий

def create_inkb_events(events, time='future'):
	inkb_events = InlineKeyboardMarkup(row_width=1)
	print(events)
	t = round(ttime.time())
	print(t, events)
	for event in events:
		if ((not event[4]) or t > event[4]):
			# Проверка, что время публикации наступило
			date = str(ut.unix_to_time(event[5])).split(' ')[0].split('-')
			name = date[2] + "." + date[1] + " "
			name += event[1]
			inkb_events.add(InlineKeyboardButton(text=name, callback_data=time+"_event_info_callback_"+str(event[7])))
	return inkb_events


# Создание клавиатуры с возможностью регистрации 
# (Все мероприятия => Тык на мероприятие => 
# => кнопки "Отмена регистрации"/"Зарегистрироваться" и "Назад к списку мероприятий")

def create_inkb_reg(user_id, event_id, addition=""):
	global dict_for_checkins
	inkb = InlineKeyboardMarkup(row_width=1)
	if db.if_user_registered(user_id, event_id):
		inkb.add(InlineKeyboardButton(text='❌ Отменить регистрацию', callback_data='unregister_user_'+str(event_id)))
		if not db.if_user_checkined(user_id, event_id):
			dict_for_checkins[user_id] = event_id
			event = search_event(user_id, event_id)
			t = round(ttime.time())
			if event[-3] < t < event[-2]:
				inkb.add(InlineKeyboardButton(text='Зачекиниться', callback_data='checkin_location_user'))
	else:
		inkb.add(InlineKeyboardButton(text='✅ Зарегистрироваться', callback_data='register_user_'+str(event_id)))
	inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data=addition+'events_callback'))
	return inkb


def create_inkb_register(user_id, event_id):
	inkb = InlineKeyboardMarkup(row_width=1)
	if (db.if_user_registered(user_id, event_id)):
		inkb.add(InlineKeyboardButton(text='❌ Отменить регистрацию', callback_data='unregister_user_'+str(event_id)))
		inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='events_callback'))
	else:
		inkb.add(InlineKeyboardButton(text='✅ Зарегистрироваться', callback_data='register_user_'+str(event_id)))
		inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='events_callback'))
	return inkb

# Создание клавиатуры чекина

dict_for_checkins = {} # user_id: event_id (ивент, на который хочет зачекиниться)


def create_inkb_checkin(user_id, event_id):
	global dict_for_checkins
	inkb = InlineKeyboardMarkup(row_width=1)
	if db.if_user_registered(user_id, event_id):
		inkb.add(InlineKeyboardButton(text='❌ Отменить регистрацию', callback_data='check_unregister_user_'+str(event_id)))
		if not db.if_user_checkined(user_id, event_id):
			dict_for_checkins[user_id] = event_id
			event = search_event(user_id, event_id)
			t = round(ttime.time())
			if event[-3] < t < event[-2]:
				inkb.add(InlineKeyboardButton(text='Зачекиниться', callback_data='checkin_location_user'))
	else:
		inkb.add(InlineKeyboardButton(text='✅ Зарегистрироваться', callback_data='check_register_user_'+str(event_id)))
	inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='checkin_events_callback'))
	return inkb

# Кнопка геолокации

location_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Поделиться локацией", request_location=True))

# Создание клавиатуры фидбэка

def create_inkb_feedback(user_id, event_id):
	inkb = InlineKeyboardMarkup(row_width=1)
	if (db.if_user_checkined(user_id, event_id) and not db.if_left_feedback(user_id, event_id)):	
		inkb.add(InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback_callback_'+str(event_id)))
	inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='past_events_callback'))
	return inkb

