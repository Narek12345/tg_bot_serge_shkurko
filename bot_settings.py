import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Redis config.
redis_host = 'localhost'
redis_port = 6379
redis_password = ''
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

# Bot config.
TOKEN = '5768840260:AAFRh6DebgtSNo33ZGwOah1VaK3E76mC4vk'
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

# DB config.
engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
