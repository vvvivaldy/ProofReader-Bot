from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

from data.config import DESCR, INSTRUCT, PREDOSTR, INFO, TRADER_HELP, SROKS, REFERRAL
from data.keyboards import kb_free, kb_instruct, kb_reg, kb_unreg, kb_prof, kb_admin, kb_black_list, kb_trader,\
     kb_keys, kb_trader2, kb_leverage, kb_subscribe_on_trader, kb_confirmation, kb_contract, kb_settings,\
     kb_set_leverage, kb_inform, kb_summ, kb_stat, kb_instruct2, kb_reg_work, kb_date, kb_admin_ref
from data.inline_keyboards import ikas, paykb, inl_kb_pr, inl_kb_status, ikk, ikst, ikb_period, ik_edit_api, \
     ikb_quantity, ikb_trader_stat, kb_order, kb_ref, kb_ref_np, inl_ref_pocent
from data.classes import Auth, Bl_Id_Trader, Bl_Id_User, UserDel, TraderStatus, UserStatus, SetUserSubscriptionStatus,\
     EditApi, EditApiTrader, Key_Duration, Activation_Quantity, Key_Delete, TraderKey, Leverage, Set_Leverage,\
     Set_Percent, Set_Dollars, Set_Sale, Set_Salary, Personal_Id, Set_Sale_Personal, Set_Salary_Personal


import logging
import sqlite3
import csv
import time as t
from datetime import date, timedelta, datetime, time
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from pybit.unified_trading import HTTP, WebSocket
from pybit import exceptions
import calendar
import dotenv
import os
import random
import string
import requests
import asyncio
import string
import decimal
from dateutil.relativedelta import relativedelta