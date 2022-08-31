"""Дать админку пользователю"""

from create_bot import dp
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from state.admin_state import FSMcreate_event, FSMmake_adm
from aiogram.dispatcher import FSMContext
import asyncio
from database.functions import if_user_login_exist, assign_admin
from keyboards.reply.admin_kb import kb_admin


@dp.message_handler(Text(equals='Дать админку'))
async def command_admin(message: types.Message):
    await message.reply('Введите логин для нового админа\n\nНапишите <code>отмена</code> чтобы закончить')
    await FSMmake_adm.new_adm.set()


@dp.message_handler(state=FSMmake_adm.new_adm)
async def make_new_adm(message: types.Message, state: FSMContext):
    adm_log = message.text
    result = assign_admin(adm_log)
    if result:
        await message.answer("Роль администратора была предоставлена!", reply_markup=kb_admin())
        await state.finish()
    else:
        await message.reply("Неправильный логин")
        await command_admin(message)

