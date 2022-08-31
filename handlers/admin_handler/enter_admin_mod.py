from create_bot import dp
from aiogram import types, Dispatcher
import database.functions as db
from keyboards.reply.admin_kb import kb_admin

@dp.message_handler(commands=['moderator'])
async def command_start(message : types.Message):
	print(f'Юзер id{message.from_user.id} нажал старт!')
	print(db.select_db("users", "*"))
	if(db.is_admin(message.from_user.id)):
		await message.answer("Менюшечка админа", reply_markup=kb_admin)
	else:
		await message.answer('Вы не являетесь админом')