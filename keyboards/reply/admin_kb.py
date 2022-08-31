from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def kb_admin():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1 = KeyboardButton('Дать админку')
    b2 = KeyboardButton('Создать мероприятие')
    b3 = KeyboardButton('Организованные мероприятия')



    markup.add(b1).add(b2).add(b3)

    return markup


def event_type():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    b4 = KeyboardButton('Online')
    b5 = KeyboardButton('MSK')
    b6 = KeyboardButton('KAZ')
    b7 = KeyboardButton('NSK')


    markup.add(b5).add(b6).add(b7).add(b4)
    return markup
