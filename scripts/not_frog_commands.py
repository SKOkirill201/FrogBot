from aiogram import Bot, types
from other.commands import all_commands
from users.save import *
import json

async def not_frog(bot: Bot, message: types.Message, users_: dict):
    global user_start_profile

    with open('other/user_profile.json', encoding='utf-8') as user_:
        profile = json.load(user_)

    # Adding person to json file | Добавление человека в json файл
    if not str(message.from_user.id) in users_:
        user_start_profile = ({str(message.from_user.id): profile})
        users_.update(user_start_profile)
    
    # /start command | Команда /start
    if str(message.text).lower() in all_commands['start']:
        photo = open('images/FrogBot 2.1 Banner.png', 'rb')
        await bot.send_photo(message.chat.id,
                             photo=photo, 
                             caption="""Добро пожаловать к нам, пользователям FrogBot'а!

Здесь вы сможете завести себе лягушку и делать многое с ней! От кормления до отправки на работу как хакера!
В общем, у нас вы не соскучитесь, ведь обновления выходят довольно часто!
                             
Пока у нас нету сайта, вы можете прописать команду /help.""",
                             message_thread_id=message.message_thread_id)
    
    # /help command | Команда /help
    elif str(message.text).lower() in all_commands['help']:
        await bot.send_message(message.chat.id, '''
<b>Важные команды</b>
 - ▶ Старт (/start) - Стартовое сообщение, вы его уже видели.
 - ❓ Хелп (/help) - Все команды.

<b>Первые взаимодействия с лягушкой</b>
 - 🐸 Взять лягушку (/get_frog) - Взять лягушку.
 - 🏷 Дать имя лягушке (/frognameset) - Вы даёте имя лягушке (Имя нужно написать в сообщении после команды).
 - 🍔 Покормить лягушку (/feed_frog) - Покормить лягушку.

<b>Информация</b>
 - ℹ Моя лягушка (/my_frog) - Информация о вашей лягушке.
 - 💸 Мой баланс (/my_balance) - Ваш баланс.

<b>Команды связанные с работой</b>
 - ⚙️ Отправить лягушку на работу (/send_frog_to_work) - Вы отправляете лягушку на работу.
 - 🔐 Выкупить лягушку из тюрьмы (/buy_frog_out_of_prison) - Если ваша лягушка в тюрьмы, вы можете выкупить её данной командой.
 - 🤝 Договориться с полицией (/negotiate_with_the_police) - Если ваша лягушка была вором, но вы хотите отправить её на работу полицейским, воспользуйтесь данной командой.

<b>Взаимодействие с другими игроками</b>
 - 💰 Отправить коины (/send_coins) - Для использования данной команды нужно написать её как ответ на сообщение пользователя которому вы хотите отправить деньги, после текста команды укажите сумму.

<b>Другое</b>
 - 🧵 Купить предметы (/buy_items) - Купить предметы для лягушки.
 - 💊 Использователь аптечку (/use_first_aid_kit) - Для использования команды нужна 1 аптечка, восстанавливает 20 здоровья.''',
        message_thread_id=message.message_thread_id,
        parse_mode=types.ParseMode.HTML)