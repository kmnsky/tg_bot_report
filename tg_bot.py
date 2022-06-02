import asyncio
from datetime import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token
from main import upload_file_fbtool, rounder, delete_files, fbtool_report, upload_file_keitaro
import os
import glob


now = datetime.now()

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Fb Report", "Fbtool", "Keitaro"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Сhoose upload", reply_markup=keyboard)


@dp.message_handler(Text(equals="Fb Report"))
async def get_fbtool_file(message: types.Message):
    await message.answer("File creation started")
    upload_file_fbtool()
    fbtool_report()
    user_id = message.from_user.id
    await bot.send_document(user_id, open(f"Fbtool_{rounder(now)}.xlsx", 'rb'))
    delete_files(f"Fbtool_{rounder(now)}.xlsx")
    delete_files("Статистика команды.xlsx")

@dp.message_handler(Text(equals="Fbtool"))
async def get_fbtool_file(message: types.Message):
    await message.answer("File creation started")
    upload_file_fbtool()
    user_id = message.from_user.id
    await bot.send_document(user_id, open("Статистика команды.xlsx", 'rb'))
    delete_files("Статистика команды.xlsx")

@dp.message_handler(Text(equals="Keitaro"))
async def get_fbtool_file(message: types.Message):
    await message.answer("File creation started")
    upload_file_keitaro()
    file_name = glob.glob('report*.csv')[0]
    user_id = message.from_user.id
    await bot.send_document(user_id, open(file_name, 'rb'))
    delete_files(file_name)

if __name__ == '__main__':
    executor.start_polling(dp)
