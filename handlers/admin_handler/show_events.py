from create_bot import dp, bot
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import os

from state.admin_state import FSMcreate_event, FSMmake_adm
from aiogram.dispatcher import FSMContext
from state.admin_state import FSMshow_events
from keyboards.inline.events_kb import make_events, make_markup, back
from database.functions import get_my_organized_events, get_register_list, get_checkin_list
from database.sqlite_db1 import select_db
from keyboards.inline.admin_events_kb import organized_events_kb, back
from utils.utils import unix_to_time


import deeplink.deeplink as dd
import utils.utils as ut




def make_csv_file(reg_list, check_list, title, admin_id):
    file_name = f'{title}-from-{admin_id}'
    reg_list = [i[0] for i in reg_list]
    check_list = [i[0] for i in reg_list]
    info_fill = "Логины зарегистрированных;Логины зачекининых\n"
    reg_n = len(reg_list)
    check_n = len(check_list)
    if reg_n >= check_n:
        for i in range(check_n):
            line = f'{reg_list[i]};{check_list[i]}\n'
            info_fill += line
        for j in range(check_n, reg_n):
            line = f'{reg_list[j]}\n'
            info_fill += line
    else:
        for i in range(reg_n):
            line = f'{reg_list[i]};{check_list[i]}\n'
            info_fill += line
        for j in range(reg_n, check_n):
            line = f'{check_list}\n'
            info_fill += line

    with open(f"data/{file_name}.csv", 'w') as file:
        file.writelines(info_fill)

    file.close()

    return f'{file_name}.csv'


def event_info(event_id):
    users_registred = get_register_list(event_id)
    user_checkined = get_checkin_list(event_id)

    return users_registred, user_checkined, len(users_registred), len(user_checkined)


@dp.message_handler(text='Организованные мероприятия')
async def command_events(message: types.Message, flag = 0):
    if flag:
        user_id = message.chat.id
    else:
        user_id = message.from_user.id
    print(user_id)
    print(message, flag)
    events = get_my_organized_events(user_id)
    print(events)
    await message.answer("<b>Организованные мероприятия</b>\n\nЧтобы получить подробную информацию - нажмите кнопку с названием интересующего вас мероприятие",
                         reply_markup=organized_events_kb(events))

"""event id	type	user_id	title description	seats_number	publication_date	date_start	data_end"""


@dp.callback_query_handler(lambda x: "event_admin" in x.data)
async def show_event_info(call: CallbackQuery):
    _, id, title, date_start, date_end = call.data.split("#")
    date_start = unix_to_time(int(date_start))
    date_end = unix_to_time(int(date_end))
    reg_list, check_list, n_reg, n_check = event_info(id)
    await call.message.edit_text(f"<b>{title}</b>\n\n<b>Даты проведения:</b> {date_start}\n<b>Дата окончания:</b> {date_end}\n\n<b>Зарегистрировано:</b> {n_reg}\n\n<b>Зачекинилось:</b> {n_check}\n\nПодробно о зарегистрированных пользователях вы можете посмотреть в приклеплённом файле",
                                 )
    file_path = make_csv_file(reg_list, check_list, title, call.from_user.id)
    await bot.send_document(call.from_user.id, open(f'data/{file_path}', 'rb'), caption='подробная информация', reply_markup=back())

    COMMAND = f"eventid_{id}"
    PATH = f"data/qrcode_{id}.png"
    dd.get_qrcode(ut.get_deeplink(COMMAND), PATH)
    qr_code = open(PATH, 'rb')
    await bot.send_photo(call.from_user.id, qr_code)
    os.remove(r'data' + f'/{file_path}')


@dp.callback_query_handler(text = 'back_e')
async def show_menu(call: CallbackQuery):
    await command_events(call.message, 1)

# выводит первые мероприятия
# @dp.message_handler(text='Мои мероприятия')
# async def command_events(message: types.Message, state: FSMContext):
#     await FSMshow_events.event.set()
#     events = admin_events(message.from_user.id)
#     event_amount = len(events)
#     if event_amount % 5 == 0:
#         parts = event_amount / 5
#     else:
#         parts = event_amount // 5 + 1
#     async with state.proxy() as data:
#         data['events'] = events
#         data['parts'] = parts
#     await message.answer('список мероприятий', reply_markup=make_markup(events, parts))
#
#
# @dp.callback_query_handler(lambda x: "SHOW" in x.text, state=FSMshow_events.event)
# async def show_more_events(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     parts = data['parts']
#     events = data['events']
#     part = int(call.data[5:])
#     await call.message.edit_text("список мероприятий", reply_markup=make_markup(events, parts, part))
#
#
# @dp.callback_query_handler(lambda x: "event" in x.text, state=FSMshow_events.event)
# async def show_event_info(call: CallbackQuery, state: FSMContext):
#
#     _, id,	type, user_id,	title,	description,	seats_number, publication_date, date_start,	data_end = call.data.split()
#     id = int(id)
#     user_id = int(user_id)
#     seats_number = int(seats_number)
#     text = f"""<b>{title}</b>\n\n{description}
#             Число мест - {seats_number}
#             Даты проведения: {date_start} - {data_end}"""
#     await call.message.edit_text(text, reply_markup=back())
#
#
# @dp.callback_query_handler(state=FSMshow_events.event, text= 'back')
# async def to_events(call: CallbackQuery, state: FSMContext):
#     await command_events(call.message, state)