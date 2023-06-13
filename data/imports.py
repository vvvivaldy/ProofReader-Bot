from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from data.config import TG_TOKEN, DESCR, INSTRUCT, PREDOSTR, PRICE, PAYMENTS_TOKEN
from data.keyboards import kb_free, kb_instruct, kb_reg, kb_unreg, kb_profile

from data.classes import Auth

import logging
import sqlite3
from datetime import date, timedelta
from pybit import spot
