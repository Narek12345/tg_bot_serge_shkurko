from sqlalchemy import Column, Integer, String
from bot_settings import Base, session


class TelegramUser(Base):
	__tablename__ = 'telegram_user'
	id = Column(Integer, primary_key=True)
	tg_id = Column(Integer)
	username = Column(String(50))


	async def register(tg_id, username):
		# We check whether the user has previously registered. If no, then register.
		if not session.query(TelegramUser).filter_by(tg_id=tg_id).first():
			new_user = TelegramUser(tg_id=tg_id, username=username)
			session.add(new_user)
			session.commit()
