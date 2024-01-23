import sys
import asyncio
import logging

from aiogram import executor

from handlers import client
from bot_settings import bot, dp, Base, engine

# Register all handlers.
client.register_client_handlers(dp)


async def on_startup(dp):
	# Creating tables in the db.
	Base.metadata.create_all(engine)


if __name__  == '__main__':
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)
	executor.start_polling(dp, on_startup=on_startup)
