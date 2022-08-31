from create_bot import dp
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from state.admin_state import FSMcreate_event, FSMmake_adm
from aiogram.dispatcher import FSMContext
from state.admin_state import FSMshow_events
from keyboards.inline.events_kb import make_events, make_markup, back
from database.sqlite_db1 import select_db
from keyboards.reply.admin_kb import kb_admin


#Папку Database, utils
@dp.message_handler(commands='moderate')
async def start_bot(message: types.Message):
    await message.answer("<b>Режим организатора</b>\nВы можете создавать и отслеживать статистику мероприятий\nа также назначать новых администраторов",
                         reply_markup=kb_admin())


@dp.message_handler(text='отмена', state='*')
async def return_to_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await start_bot(message)
