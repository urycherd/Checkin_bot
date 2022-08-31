from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

"""id	type	user_id	title	description	seats_number	publication_date	date_start	data_end"""


def organized_events_kb(events):
    markup = InlineKeyboardMarkup()
    """['type', 'title', 'description', 'seats_number', 'publication_date', 'data_start', 'data_end', 'id'],"""
    for e in events:
        title = e[1]
        info = f'event_admin#{e[-1]}#{e[1]}#{e[-3]}#{e[-2]}'
        btn = InlineKeyboardButton(title, callback_data=info)
        markup.add(btn)

    return markup

def back():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('⬅ Назад к списку мероприятий', callback_data='back_e')
    markup.add(btn)

    return markup




