from aiogram.dispatcher.filters.state import State, StatesGroup


class InterrogationFSM(StatesGroup):
	marketplace = State()
	evaluation = State()


class FeedbackFSM(StatesGroup):
	text = State()