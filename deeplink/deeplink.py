from aiogram import types
import qrcode

from database.functions import *
from keyboards.client_kb import create_inkb_reg, create_event_description_message, search_event


def handle_deeplink(message: types.Message):
    text = message.text.replace("/start ", "")
    user_id = message.from_user.id
    command = text.split("_")
    if command[0] == "eventid":
        event_id = command[1]
        if if_user_id_exist(user_id):
            if not if_user_registered(user_id, event_id):
                register_user(user_id, event_id)
            if not if_user_checkined(user_id, event_id):
                user_checkined(user_id, command[1])
            return (f"""<b>Вы успешно зачекинены!</b>
                    {create_event_description_message(search_event(user_id, int(event_id)))}""",
                    create_inkb_reg(user_id, event_id, "checkin_"))
    return


def get_qrcode(data, path):
    img = qrcode.make(data)
    img.save(path)

