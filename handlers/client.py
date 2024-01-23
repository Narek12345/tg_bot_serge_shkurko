import redis

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot_settings import bot, dp, redis_client
from fsm.client_fsm import InterrogationFSM, FeedbackFSM
from keyboards.client_keyboards import SelectMarketplaceKeyboard, EvaluationKeyboard
from db.client_db import TelegramUser


async def send_message(message: Message):
	await message.answer('message')


async def cmd_start(message: Message):
	"""Command to launch the bot. Together with the link we take the article."""
	# Check thet the article was transmitted.
	if len(message.text) > 6:
		# Register the user in the db.
		await TelegramUser.register(message.from_user.id, message.from_user.username)

		# Save the product article in redis.
		article = message.text.replace('/start ', '')
		redis_client.set(str(message.from_user.id), article)
		
		await InterrogationFSM.marketplace.set()
		await message.answer('Где вы сделали заказ?', reply_markup=SelectMarketplaceKeyboard.marketplace_keyboard)
	else:
		# Article not transmitted.
		await message.answer('Пожалуйста, перейдите по ссылке с артиклем!')


async def process_marketplace(query: CallbackQuery, state: FSMContext):
	"""Process marketplace."""
	answer = query.data[-1]

	# Checking the marketplace.
	if answer == 1:
		async with state.proxy() as data:
			data['marketplace'] = 'Wildberries'
	elif answer == 2:
		async with state.proxy() as data:
			data['marketplace'] = 'OZON'
	elif answer == 3:
		async with state.proxy() as data:
			data['marketplace'] = 'Kazan Express'
	
	await InterrogationFSM.evaluation.set()
	await query.message.answer('Оцените на сколько вам понравился товар', reply_markup=EvaluationKeyboard.evaluation_keyboard)
	await query.answer()


async def process_evaluation(query: CallbackQuery, state: FSMContext):
	"""Process evaluation."""
	# Write data to the db before clearning it in temporary memory.
	await state.finish()
	
	answer = int(query.data[-1])

	if answer <= 3:
		# If the rating is less than or equalto 3.
		await FeedbackFSM.text.set()
		await query.message.answer('Что не понравилось?')
	else:
		# If the rating is more than 3. Please rate our product.
		article = redis_client.get(str(query.from_user.id))
		await query.message.answer('https://ozon.ru')

	await query.answer()


async def process_feedback(message: Message, state: FSMContext):
	"""Process feedback."""
	text = message.text
	await message.answer('Мы свяжемся с вами в ближайшее время и решим проблему!')
	await state.finish()


def register_client_handlers(dp):
	dp.register_message_handler(send_message, commands='send_message')
	dp.register_message_handler(cmd_start, commands='start')
	dp.register_callback_query_handler(process_marketplace, lambda query: query.data.startswith('process_marketplace'), state=InterrogationFSM.marketplace)
	dp.register_callback_query_handler(process_evaluation, lambda query: query.data.startswith('process_evaluation'), state=InterrogationFSM.evaluation)
	dp.register_message_handler(process_feedback, state=FeedbackFSM.text)
