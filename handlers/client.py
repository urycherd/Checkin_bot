from aiogram import types, Dispatcher
from create_bot import bot, dp
import keyboards.client_kb as kb
from aiogram.dispatcher.filters import Text
import database.functions as db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import utils.utils as ut
import deeplink.deeplink as dd

# =====================Первичная регистрация юзера через фсм===============================================

class FSMRegister_user(StatesGroup):
	login = State()
	campus = State()


@dp.message_handler(state="*", commands='cancel')
async def cancel_handler(message : types.Message, state: FSMContext):
	current_state = await state.get_state()
	if (current_state is None):
		return
	await state.finish()
	await message.reply('Отменили', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
	print(f'Юзер id{message.from_user.id} нажал старт!')
	print(db.select_db("users", "*"))
	if message.text[:7] == "/start ":
		res = dd.handle_deeplink(message)
		if res:
			await message.answer(text=res[0], reply_markup=res[1])
			return
	if(db.if_user_id_exist(message.from_user.id)):
		await message.answer(f"Привет, {db.get_login(message.from_user.id)}", reply_markup=kb.base_kb_client)
	else:
		await FSMRegister_user.login.set()
		await message.reply('Введи свой логин\n(напиши /cancel, если не хочешь регистрироваться)')


@dp.message_handler(state=FSMRegister_user.login)
async def get_login(message: types.Message, state: FSMContext):
	async with state.proxy() as log_data:
		log_data['login'] = message.text
	await FSMRegister_user.next()
	await message.reply('Выбери свой кампус\n(напиши /cancel, если не хочешь регистрироваться)', reply_markup=kb.kb_campus)


@dp.message_handler(state=FSMRegister_user.campus)
async def get_login(message: types.Message, state: FSMContext):
	if (message.text != "MSK" and message.text != "KAZ" and message.text != "NSK"):
		await FSMRegister_user.campus.set()
		await message.reply('Неправильный формат кампуса :(\nПопробуй тыкнуть на кнопку!', reply_markup=kb.kb_campus)
		return
	async with state.proxy() as log_data:
		log_data['campus'] = message.text
	await state.finish()
	if db.addnewuser(message.from_user.id, log_data['login'], log_data['campus']):
		await message.answer('Регистрация успешно завершена! Теперь вы можете регистрироваться и чекиниться на мероприятиях!', reply_markup=kb.base_kb_client)
	else:
		await message.answer('Не получилось зарегистрироваться :(\nПопробуй ещё раз /start')

		
# =====================Базовая клавиатура пользователя + команды через /===============================================

@dp.message_handler(commands=['events'])
@dp.message_handler(Text(equals="Все мероприятия"))
async def command_events(message : types.Message):
	print(message.from_user.id)
	print(db.if_user_id_exist(message.from_user.id))
	print(db.select_db("users", "*"))
	print(db.select_db("event", "*"))
	print("->", message.from_user.id)
	print(db.get_relevant_events(message.from_user.id))
	await message.answer('Список будущих мероприятий', reply_markup=kb.create_inkb_events(db.get_relevant_events(message.from_user.id)))


@dp.message_handler(commands=['timetable'])
@dp.message_handler(Text(equals="Моё расписание"))
async def command_timetable(message : types.Message):
	await message.answer('Список мероприятий, на которые вы зарегистрированы', reply_markup=kb.create_inkb_events(db.get_future_user_events(message.from_user.id), 'checkin'))


@dp.message_handler(commands=['past_events'])
@dp.message_handler(Text(equals="Прошедшие события"))
async def command_past_events(message : types.Message):
	print(message.from_user.id)
	await message.answer('Список мероприятий, на которых ты был', reply_markup=kb.create_inkb_events(db.get_past_user_events(message.from_user.id), 'past'))

# ========================================ИНЛАЙН======================================================================

# events = db.get_relevant_events(user_id) - список будущих ивентов, на которые пользователь потенциально может зарегаться (или уже зареган)
# my_events = db.get_future_user_events(user_id) - список будущих ивентов, на которые зареган пользователь

# callback.message.chat.id - ID телеграм юзера


@dp.callback_query_handler(text='events_callback')
async def query_command_events(callback : types.CallbackQuery):
	await callback.message.edit_text("Список будущих мероприятий", reply_markup=kb.create_inkb_events(db.get_relevant_events(callback.message.chat.id)))


@dp.callback_query_handler(text='past_events_callback')
async def query_command_events(callback : types.CallbackQuery):
	await callback.message.edit_text("Список прошедших мероприятий", reply_markup=kb.create_inkb_events(db.get_past_user_events(callback.message.chat.id), 'past'))


@dp.callback_query_handler(text='checkin_events_callback')
async def query_command_events(callback : types.CallbackQuery):
	await callback.message.edit_text("Список будущих мероприятий, на которые Вы зарегистрированы", reply_markup=kb.create_inkb_events(db.get_future_user_events(callback.message.chat.id), 'checkin')) # my_events




@dp.callback_query_handler(Text(startswith='future_event_info_callback_'))
async def event_info_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[4])
	id_ = callback.message.chat.id
	await callback.message.edit_text(kb.create_event_description_message(kb.search_event(id_, event_id)), reply_markup=kb.create_inkb_reg(id_, event_id))
	await callback.answer()


@dp.callback_query_handler(Text(startswith='past_event_info_callback_'))
async def event_info_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[4])
	id_ = callback.message.chat.id
	time = callback.data.split('_')[0]
	# print("mem, kek, ", id_, event_id)
	await callback.message.edit_text(kb.create_event_description_message(kb.search_event(id_, event_id, time)), reply_markup=kb.create_inkb_feedback(id_, event_id))
	await callback.answer()


@dp.callback_query_handler(Text(startswith='checkin_event_info_callback_'))
async def event_info_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[4])
	id_ = callback.message.chat.id
	await callback.message.edit_text(kb.create_event_description_message(kb.search_event(id_, event_id)), reply_markup=kb.create_inkb_reg(id_, event_id, "checkin_"))
	await callback.answer()





@dp.callback_query_handler(Text(startswith='unregister_user_'))
async def unregister_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[2])
	user_id = callback.message.chat.id
	event = kb.search_event(user_id, event_id)
	if (db.unregister_user(user_id, event_id)):
		await callback.message.edit_text(kb.create_event_description_message(event), reply_markup=kb.create_inkb_reg(user_id, event_id))
	else:
		await callback.message.answer('Не получилось отменить регистрацию, попробуйте ещё раз', reply_markup=kb.create_inkb_reg(user_id, event_id))



@dp.callback_query_handler(Text(startswith='register_user_'))
async def unregister_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[2])
	user_id = callback.message.chat.id
	event = kb.search_event(user_id, event_id)
	if (db.register_user(user_id, event_id)): 
		await callback.message.edit_text(kb.create_event_description_message(event), reply_markup=kb.create_inkb_reg(user_id, event_id))
	else:
		await callback.message.edit_text('Не получилось зарегистрироваться, попробуйте ещё раз', reply_markup=kb.create_inkb_reg(user_id, event_id))


# =======================Checkin=====================================================================================



@dp.callback_query_handler(Text(equals='checkin_location_user'))
async def checkin_callback(callback : types.CallbackQuery):
	await callback.message.answer('Чтобы сделать чекин нужно поделиться своей локацией', reply_markup=kb.location_kb)


@dp.callback_query_handler(Text(startswith='checkin_unregister_user_'))
async def check_unregister_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[3])
	user_id = callback.message.chat.id
	event = kb.search_event(user_id, event_id)
	if (db.unregister_user(user_id, event_id)):
		await callback.message.edit_text(kb.create_event_description_message(event), reply_markup=kb.create_inkb_reg(user_id, event_id, "checkin_"))
	else:
		await callback.message.answer('Не получилось отменить регистрацию, попробуйте ещё раз', reply_markup=kb.create_inkb_reg(user_id, event_id, "checkin_"))


@dp.callback_query_handler(Text(startswith='checkin_register_user_'))
async def check_register_callback(callback : types.CallbackQuery):
	event_id = int(callback.data.split('_')[3])
	user_id = callback.message.chat.id
	event = kb.search_event(user_id, event_id)
	if (db.register_user(user_id, event_id)):
		await callback.message.edit_text(kb.create_event_description_message(event), reply_markup=kb.create_inkb_reg(user_id, event_id, "checkin_"))
	else:
		await callback.message.edit_text('Не получилось зарегистрироваться, попробуйте ещё раз')
		await callback.message.answer(kb.create_event_description_message(event), reply_markup=kb.create_inkb_reg(user_id, event_id, "checkin_"))


@dp.message_handler(content_types=['location'])
async def handle_location(message : types.Message):
	global dict_for_checkins
	user_id = message.from_user.id
	event_id = kb.dict_for_checkins[user_id]
	lat = message.location.latitude
	lon = message.location.longitude
	print(f"lat = {lat}\nlon = {lon}")
	campus = db.get_user_campus(message.from_user.id)
	if (ut.check_coordinates([lat, lon], ut.campus_coordinates(campus))):
		await message.answer('Чекин произошёл успешно✅', reply_markup=kb.base_kb_client)
		db.user_checkined(user_id, event_id)
	else:
		await message.answer('Ты не в кампусе :(', reply_markup=kb.base_kb_client)
	await message.answer('Список мероприятий, на которые вы зарегистрированы', reply_markup=kb.create_inkb_events(db.get_future_user_events(message.from_user.id)))



# =================Feedback FSM==========================НЕ РАБОТАИТТТ==================================

class FSMfeedback(StatesGroup):
	eval = State()
	text = State()

dict_for_feedbacks = {} # user_id: event_id (ивент, на который хочет отправить отзыв)


@dp.callback_query_handler(Text(startswith='feedback_callback_'))
async def feedback_handler(callback : types.CallbackQuery):
	global dict_for_feedbacks
	event_id = int(callback.data.split('_')[2])
	dict_for_feedbacks[callback.message.chat.id] = event_id
	await FSMfeedback.eval.set()
	await callback.message.reply('Насколько тебе понравилось мероприятие от 0 до 5?\n(напиши /cancel, если не хочешь оставлять фидбэк)', reply_markup=kb.kb_numbers)


@dp.message_handler(state=FSMfeedback.eval)
async def get_feedback_eval(message: types.Message, state: FSMContext):
	if message.text not in [str(i) for i in range(6)]:
		await message.reply("Введи целое число от 0 до 5 включительно\n(напиши /cancel, если не хочешь оставлять фидбэк)", reply_markup=kb.kb_numbers)
		# await FSMfeedback.eval.set()
		return
	async with state.proxy() as feedback_data:
		feedback_data['eval'] = message.text
	await FSMfeedback.next()
	await message.reply('Напиши развёрнутый фидбэк :з\n(напиши /cancel, если не хочешь регистрироваться)')


@dp.message_handler(state=FSMfeedback.text)
async def get_feedback_eval(message: types.Message, state: FSMContext):
	global dict_for_feedbacks
	user_id = message.from_user.id
	async with state.proxy() as feedback_data:
		feedback_data['text'] = message.text
	# print('feedback generated: ', feedback_data)
	if db.leave_feedback(user_id, dict_for_feedbacks[user_id], int(feedback_data['eval']), feedback_data['text']):
		await message.answer('Спасибо за отзыв!', reply_markup=kb.base_kb_client)
		await message.answer("Список прошедших мероприятий", reply_markup=kb.create_inkb_events(db.get_past_user_events(user_id), 'past'))
	else:
		await message.answer('Не получилось оставить отзыв :(', reply_markup=kb.base_kb_client)
	await state.finish()
