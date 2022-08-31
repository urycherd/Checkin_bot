from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

"""id	type	user_id	title	description	seats_number	publication_date	date_start	data_end"""


# делит список events на parts частей
def make_events(events):
    event_amount = len(events)
    if event_amount % 5 == 0:
       parts = event_amount / 5
    else:
       parts = event_amount // 5 + 1

    markup = make_markup(events, parts)
    return markup



def make_info(line):
    data = "event " + " ".join([str(i) for i in line])
    return data


"""Подаёт клаву с 5 ивентами, в callback - инфа про мероприятия"""


def make_markup(events, parts, part=1):
    markup = InlineKeyboardMarkup()
    left = (part - 1) * 5 + 1
    right = part*5 + 1
    for event_index in range(left, right):
        event = events[event_index]
        title = event[3]
        data = make_info(event)
        button = InlineKeyboardButton(title, callback_data=data)
        markup.row(button)
    button_left = InlineKeyboardButton("<", callback_data=f'show {part - 1}')
    button_right = InlineKeyboardButton(">", callback_data=f'show {part + 1}')
    if part == 1:
        button_left = InlineKeyboardButton(".", callback_data='end')
    if part == parts:
        button_right = InlineKeyboardButton(".", callback_data='end')

    button = InlineKeyboardButton("Отмена", callback_data='back')

    markup.row(button_left, button, button_right)
    return markup


def back():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('назад', callback_data='back')
    markup.add(btn)

    return markup



# """id	type	user_id	title	description	seats_number	publication_date	date_start	data_end"""
#
# a = [1, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19']
#
# f = ''
# for i in a:
#     f += f'{str(i)} '
#
# id,	type,user_id,	title,	description,	seats_number, publication_date, date_start,	data_end = f.split()
# id = int(id)
# user_id = int(user_id)
# seats_number = int(seats_number)

events = [
    [1, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
    [2, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[3, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[4, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[5, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[6, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[7, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[8, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[9, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[10, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[11, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[12, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[13, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
[14, "КЗН", 543, "good", 'description', 23, '2022-09-19', '2022-09-19', '2022-09-19'],
]
# num = len(events)
#
# if num % 5 == 0:
#     parts = num/5
# else:
#     parts = num // 5 + 1
#
#
#
# print(parts)
#
# database = "event " + " ".join([str(i) for i in events[0]])
#
# print(database.split())

