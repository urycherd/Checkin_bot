from create_bot import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from state.admin_state import FSMcreate_event
from aiogram.dispatcher import FSMContext
from keyboards.reply.admin_kb import kb_admin, event_type
from database.functions import addnewevent
from utils.utils import time_to_unix


# ------------опция "создать мероприятие"
@dp.message_handler(Text(equals='Создать мероприятие'), state=None)
async def command_fsm(message: types.Message):
    await FSMcreate_event.title.set()
    await message.reply('Введите название мероприятия\n<i>Для отмены напишите "отмена"</i>')


@dp.message_handler(state=FSMcreate_event.title)
async def load_event_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
      data['title'] = message.text
    await FSMcreate_event.next()
    await message.reply('Опишите мероприятие')


@dp.message_handler(state=FSMcreate_event.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
      data['description'] = message.text
    await FSMcreate_event.next()
    await message.reply('Теперь укажите дату и время <b>начала</b> мероприятия в формате\n<code>YYYY-MM-DD HH:MM</code>')


@dp.message_handler(state=FSMcreate_event.data_start)
async def load_start_time(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['data_start'] = time_to_unix(message.text)
        await FSMcreate_event.next()
        await message.reply('Теперь укажите дату и время <b>окончания</b> мероприятия в формате\n<code>YYYY-MM-DD HH:MM</code>')
    except Exception:
        await message.reply("Формат даты неверен")


@dp.message_handler(state=FSMcreate_event.data_end)
async def load_end_time(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['data_end'] = time_to_unix(message.text)
        await FSMcreate_event.next()
        await message.reply('Укажите <b>время публикации мероприятия</b> в формате\n<code>YYYY-MM-DD HH:MM</code>')
    except Exception:
        await message.reply("Формат даты неверен")


@dp.message_handler(state=FSMcreate_event.date_public)
async def load_date_public(message: types.Message, state: FSMContext):
    try:
        if message.text == '_':
            t = '2000-01-01 00:00'
        else:
            t = message.text
        async with state.proxy() as data:
            data['date_public'] = time_to_unix(t)
        await FSMcreate_event.next()
        await message.reply('Выберите подходящий формат вашего мероприятия\nОнлайн или город',
                        reply_markup=event_type())
    except Exception:
        await message.reply("Формат даты неверен")


@dp.message_handler(state=FSMcreate_event.type)
async def load_format(message: types.Message, state: FSMContext):
    if (message.text != 'Online' and message.text != 'NSK' and message.text != 'KAZ' and message.text != 'MSK'):
        await FSMcreate_event.type.set()
        await message.reply('Формат отсутствует', reply_markup=event_type())
        return
    async with state.proxy() as data:
        data['type'] = message.text
    await FSMcreate_event.next()
    await message.answer("Напишите максимально количество участников\nФормат - число")


@dp.message_handler(state=FSMcreate_event.seats_number)
async def load_seats_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        type = data['type']
        user_id = message.from_user.id
        title = data['title']
        seats_number = int(message.text)
        data_start = data['data_start']
        data_end = data['data_end']
        description = data['description']
        publication_date = data['date_public']
        addnewevent(type, user_id, title, seats_number, data_start, data_end, description, publication_date)
        await message.reply('Вы зарегистрировали мероприятие!', reply_markup=kb_admin())
    except Exception:
        await message.reply('К сожалению, не удалось зарегистрировать мероприятие(', reply_markup=kb_admin())
    await state.finish()
