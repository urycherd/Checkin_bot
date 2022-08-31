from aiogram.utils import executor
from create_bot import dp
import handlers

async def on_start(_):
	print('Бот запустився')


from handlers import client #, admin, other

# client.register_handlers_client(dp)
# admin.register_handlers_admin(dp)
# other.register_handlers_other(dp) # Обязательно последний! Т.к. принимает в себя любые сообщения

executor.start_polling(dp, skip_updates=True, on_startup=on_start)