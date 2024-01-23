from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class SelectMarketplaceKeyboard:
	marketplace_1 = InlineKeyboardButton('Wildberries', callback_data='process_marketplace_1')
	marketplace_2 = InlineKeyboardButton('OZON', callback_data='process_marketplace_1')
	marketplace_3 = InlineKeyboardButton('Kazan Express', callback_data='process_marketplace_1')

	marketplace_keyboard = InlineKeyboardMarkup().add(marketplace_1).add(marketplace_2).add(marketplace_3)


class EvaluationKeyboard:
	but_1 = InlineKeyboardButton('1', callback_data='process_evaluation_1')
	but_2 = InlineKeyboardButton('2', callback_data='process_evaluation_2')
	but_3 = InlineKeyboardButton('3', callback_data='process_evaluation_3')
	but_4 = InlineKeyboardButton('4', callback_data='process_evaluation_4')
	but_5 = InlineKeyboardButton('5', callback_data='process_evaluation_5')

	evaluation_keyboard = InlineKeyboardMarkup().row(but_1, but_2, but_3, but_4, but_5)