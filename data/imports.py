from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from data.config import DESCR, INSTRUCT, PREDOSTR, PRICE
from data.keyboards import kb_free, kb_instruct, kb_reg, kb_unreg, kb_profile, kb_admin
from data.keyboards import _

from data.classes import Auth

import logging
import sqlite3
from datetime import date, timedelta
from cryptography.fernet import Fernet
from pybit.unified_trading import HTTP
from pybit import exceptions
from dotenv import load_dotenv
import os