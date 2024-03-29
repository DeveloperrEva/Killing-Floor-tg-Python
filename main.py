import re
import logging
import sqlite3
from datetime import date
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import db as db
import servers as srv
import players as pl
import config
from filters import IsAdmin

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
today = date.today()
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

class Mail(StatesGroup):
    photo = State()
    description = State()

class Send(StatesGroup):
    video = State()
    description = State()

inline_btn = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
back = InlineKeyboardMarkup().add(inline_btn)

# Старт

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db.join(
        chat_id=message.from_user.id,
        username=message.from_user.username,
        firstname=message.from_user.first_name,
        date=today
    )

    markup = InlineKeyboardMarkup(row_width=2)
    item1 = InlineKeyboardButton("ℹ️ Список серверов", callback_data="kf")
    markup.add(item1)

    full_message = f'<b>🙋🏻‍♂️ Добро пожаловать в бота для мониторинга серверов KF Sunrise Project</b>'
    
    full_message_admin = f'<b>Пользователь запустил бота -> @{message.from_user.username} ->{message.from_user.id}</b>'

    await bot.send_message(
        message.from_user.id,
        full_message,
        reply_markup=markup
    )

    await bot.send_message(
        config.admin_logs,
        full_message_admin,
    )

@dp.callback_query_handler(lambda c: c.data == "kf")
async def servers(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=2)
    item1 = InlineKeyboardButton("KF-Masters", callback_data="masters")
    item2 = InlineKeyboardButton("KF-HzD", callback_data="hzd")
    item3 = InlineKeyboardButton("KF-Massacre", callback_data="massacre")
    markup.add(item1, item2, item3)

    await callback_query.message.edit_text(
        text=f'<b>🌐 Выберите сервер...</b>',
        reply_markup=markup
        )
    
@dp.callback_query_handler(lambda c: c.data == "masters")
async def masters(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    item1 = InlineKeyboardButton("Список игроков", callback_data="players_masters")
    item2 = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
    markup.add(item1, item2)
    
    data = await srv.get_server_info_masters()
    
    ip = data['result']['address']
    maps = data['result']['map']['name']
    status = data['result']['status']
    online = data['result']['players']['now']
    online_max = data['result']['players']['max']
    
    if status == 1:
        status = '✅ Работает'
    else:
        status = '❌ Не работает'

    matches = re.findall(r"[A-Z].*", maps)
    if matches:
        replace = matches[0]

    await callback_query.message.edit_text(
        text=f'🧟‍♀️ Сервер KF-Masters\n\n,'
             f'🌐 IP-Адрес: <b>{ip}</b>\n\n'
             f'💠 Статус сервера: <b>{status}</b>\n\n'
             f'🃏 Карта: <b>{replace}\n\n</b>'
             f'👤Игроков онлайн: <b>{online}/{online_max}</b>\n\n',
        reply_markup=markup
    )
    
@dp.callback_query_handler(lambda c: c.data == "hzd")
async def hzd(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    item1 = InlineKeyboardButton("Список игроков", callback_data="players_hzd")
    item2 = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
    markup.add(item1, item2)
    
    data = await srv.get_server_info_hzd()
    
    ip = data['result']['address']
    maps = data['result']['map']['name']
    status = data['result']['status']
    online = data['result']['players']['now']
    online_max = data['result']['players']['max']
    
    if status == 1:
        status = '✅ Работает'
    else:
        status = '❌ Не работает'

    matches = re.findall(r"[A-Z].*", maps)
    if matches:
        replace = matches[0]

    await callback_query.message.edit_text(
        text=f'🧟‍♀️ Сервер KF-HzD\n\n,'
             f'🌐 IP-Адрес: <b>{ip}</b>\n\n'
             f'💠 Статус сервера: <b>{status}</b>\n\n'
             f'🃏 Карта: <b>{replace}\n\n</b>'
             f'👤Игроков онлайн: <b>{online}/{online_max}</b>\n\n',
        reply_markup=markup
    )
    
@dp.callback_query_handler(lambda c: c.data == "massacre")
async def massacre(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    item1 = InlineKeyboardButton("Список игроков", callback_data="players_massacre")
    item2 = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
    markup.add(item1, item2)
    
    data = await srv.get_server_info_massacre()
    
    ip = data['result']['address']
    maps = data['result']['map']['name']
    status = data['result']['status']
    online = data['result']['players']['now']
    online_max = data['result']['players']['max']
    
    if status == 1:
        status = '✅ Работает'
    else:
        status = '❌ Не работает'

    matches = re.findall(r"[A-Z].*", maps)
    if matches:
        replace = matches[0]

    await callback_query.message.edit_text(
        text=f'🧟‍♀️ Сервер KF-Massacre\n\n,'
             f'🌐 IP-Адрес: <b>{ip}</b>\n\n'
             f'💠 Статус сервера: <b>{status}</b>\n\n'
             f'🃏 Карта: <b>{replace}\n\n</b>'
             f'👤Игроков онлайн: <b>{online}/{online_max}</b>\n\n',
        reply_markup=markup
    )

# Список игроков

@dp.callback_query_handler(lambda c: c.data == "players_masters")
async def masters(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    item2 = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
    markup.add(item2)

    server_players = await pl.get_server_player_masters()

    arr = []
    for player in server_players['result']:
        name = arr.append(player["name"])
        players = "\n".join(arr)

        await callback_query.message.edit_text(
        text=f'🧟‍♀️ Список игроков на сервере KF-Masters\n\n'
             f'🌐 Игроки:\n\n'
             f'<b>{players}</b>\n\n',
        reply_markup=markup
    )

@dp.callback_query_handler(lambda c: c.data == "players_hzd")
async def hzd(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    item2 = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
    markup.add(item2)

    server_players = await pl.get_server_player_hzd()


    arr = []
    for player in server_players['result']:
        name = arr.append(player["name"])
        players = "\n".join(arr)

    await callback_query.message.edit_text(
        text=f'🧟‍♀️ Список игроков на сервере KF-HzD\n\n'
             f'🌐 Игроки:\n\n'
             f'<b>{players}</b>\n\n',
        reply_markup=markup
    )

@dp.callback_query_handler(lambda c: c.data == "players_massacre")
async def massacre(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    item2 = InlineKeyboardButton('⬅️ Назад', callback_data='kf')
    markup.add(item2)

    server_players = await pl.get_server_player_masters()
    
    arr = []
    for player in server_players['result']:
        name = arr.append(player["name"])
        players = "\n".join(arr)

        await callback_query.message.edit_text(
        text=f'🧟‍♀️ Список игроков на сервере KF-Massacre\n\n'
             f'🌐 Игроки:\n\n'
             f'<b>{players}</b>\n\n',
        reply_markup=markup
    )

# Админка

@dp.message_handler(IsAdmin(), commands=['admin'], state="*")
async def admin(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=2)
    item1 = InlineKeyboardButton("Статистика", callback_data="stats")
    item2 = InlineKeyboardButton("Рассылка", callback_data="send_all")
    item3 = InlineKeyboardButton("Рассылка (с видео)", callback_data="send_all_video")
    markup.add(item1, item2, item3)

    full_message = f'Выберите опцию:'

    await bot.send_message(
        message.from_user.id,
        full_message,
        reply_markup=markup
    )

@dp.callback_query_handler(lambda c: c.data == "stats")
async def get_stats(callback_query: types.CallbackQuery):
    all_user, day_user = db.all_users()
    await bot.send_message(
        callback_query.message.chat.id,
        f"Пользователи за все время: {all_user}\n\nПользователи за сегодня: {day_user}"
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == "send_all")
async def mail(callback_query: types.CallbackQuery):
        await Mail.photo.set()
        await callback_query.message.answer('''<b>📷 Загрузите фото рассылки

<i>Для пропуска напишите "-"</i></b>''')

@dp.message_handler(content_types=['photo'], state=Mail.photo)
async def mail2(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            try:
                data['photo'] = message.photo[0].file_id
            except:
                data['photo'] = None

        await Mail.next()
        await message.answer('''<b>✉️ Теперь введите текст рассылки

<i>Поддержка разметки "HTML"</i></b>''')

@dp.message_handler(state=Mail.photo)
async def mail2(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            try:
                data['photo'] = message.photo[0].file_id
            except:
                data['photo'] = None
        await Mail.next()
        await message.answer('''<b>✉️ Теперь введите текст рассылки

<i>Поддержка разметки "HTML"</i></b>''')

@dp.message_handler(state=Mail.description)
async def mail3(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['description'] = message.text
            g, e = 0, 0
            for user in db.all_users_send():
                try:
                    await bot.send_photo(user[0], data['photo'], data['description'], parse_mode='html')
                    g += 1
                except:
                    try:
                        await bot.send_message(user[0], data['description'], parse_mode='html')
                        g += 1
                    except:
                        e += 1

        await state.finish()
        await message.answer(f'''<b>⏱ Рассылка окончена!

👍 Получили сообщение:</b> <code>{g}</code>
<b>👎 Не получили:</b> <code>{e}</code>''')

@dp.callback_query_handler(lambda c: c.data == "send_all_video")
async def video(callback_query: types.CallbackQuery):
        await Send.video.set()
        await callback_query.message.answer('''<b>📷 Загрузите видео</b>''')

@dp.message_handler(content_types=['video'], state=Send.video)
async def video2(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['video'] = message.video[0].file_id
        await Send.next()
        await message.answer('''<b>✉️ Теперь введите текст рассылки

<i>Поддержка разметки "HTML"</i></b>''')

@dp.message_handler(state=Send.video)
async def video2(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['video'] = message.video[0].file_id
        await Send.next()
        await message.answer('''<b>✉️ Теперь введите текст рассылки

<i>Поддержка разметки "HTML"</i></b>''')

@dp.message_handler(state=Send.description)
async def video3(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['description'] = message.text
            g, e = 0, 0
            for user in db.all_users_send():
                await bot.send_video(user[0], data['video'], data['description'], parse_mode='html')
                g += 1

        await state.finish()
        await message.answer(f'''<b>⏱ Рассылка окончена!

👍 Получили сообщение:</b> <code>{g}</code>
<b>👎 Не получили:</b> <code>{e}</code>''')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)