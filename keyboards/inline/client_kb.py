from urllib import request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types
from create_bot import dp, bot

b1 = KeyboardButton("Все мероприятия")
b2 = KeyboardButton("Сделать чекин")
b3 = KeyboardButton("Прошедшие события")
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)

base_kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
base_kb_client.add(b1).add(b2).add(b3)

# =========================Inline buttons=========================================

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

def create_inkb_events(events):
	inkb_events = InlineKeyboardMarkup(row_width=1)
	for event in events:
		inkb_events.add(InlineKeyboardButton(text=event[0], callback_data=event[1]))
	return inkb_events


def create_inkb_register():
	inkb = InlineKeyboardMarkup(row_width=1)
	if (True):			# Если пользователь зареган (заменить потом на Сашину функцию if_user_registered(user_id, event_id))
		inkb.add(InlineKeyboardButton(text='❌ Отменить регистрацию', callback_data='unregister_user'))
		inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='events_callback'))
	else:
		inkb.add(InlineKeyboardButton(text='✅ Зарегистрироваться', callback_data='register_user'))
		inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='unregister_user'))
	return inkb


def create_inkb_checkin():
	inkb = InlineKeyboardMarkup(row_width=1)
	if (True):			# Если пользователь не зачекинен на мероприятии (заменить на Сашину функцию if_user_checkined(user_id, event_id))
		inkb.add(InlineKeyboardButton(text='Сделать чекин', callback_data='checkin_location_user'))
	inkb.add(InlineKeyboardButton(text='⬅ Назад к списку мероприятий', callback_data='my_events_callback'))
	return inkb


def create_event_description_message(event):
	res = "<b>Название мероприятия: </b>"
	res += event[0]
	res += "\n\n<b>Описание: </b>"
	res += event[2]
	return res


location_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Поделиться локацией", request_location=True))