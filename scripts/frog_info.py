from aiogram import Bot, types
from other.commands import all_commands

import logging
import datetime

cdate = datetime.datetime.now()

logging.basicConfig(level=logging.INFO)

async def frog_info_commands(bot: Bot, message: types.Message, users_: dict, config: dict):
    if str(message.text).lower() in all_commands['my_frog']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            print(f'Пользователь {message.from_user.id} посмотрел информацию о своей лягушке')
            if message.from_user.username.lower() in ('', None, '@', 'none'):
                user_frog = f'Ваша лягушка'
            else:
                user_frog = f'Лягушка пользователя <a href="t.me/{message.from_user.username}">{message.from_user.username}</a>'
            ranks_values = config['ranks_values']
            
            text1 = '\n🧵 Предметы'
            items = f''''''
            items_count = 0

            for item in list(users_[str(message.from_user.id)]['frog']['items'].keys()):
                if users_[str(message.from_user.id)]['frog']['items'][item]['player_has'] == True:
                    level = users_[str(message.from_user.id)]['frog']['items'][item]['level']
                    text = config['items'][item]
                    items += f'\n - {text} {level} уровня'
                    items_count += 1
            itemstext = f'({items_count}):'
            if items == f'''''':
                items = ''
                text1 = ''
                itemstext = ''

            event_items = ''''''
            if users_[str(message.from_user.id)]['user']['event_items']['has_event_items'] == True:
                event_items += '\n🆕 Ивентные валюты/предметы:'
                if users_[str(message.from_user.id)]['user']['event_items']['candy_2023'] > 0:
                    candy_2023 = users_[str(message.from_user.id)]['user']['event_items']['candy_2023']
                    event_items += f'\n - 🍭 Конфеты: {candy_2023}'
                if users_[str(message.from_user.id)]['user']['cases'] > 0:
                    cases = users_[str(message.from_user.id)]['user']['cases']
                    event_items += f'\n - ❓ Кейсы: {cases}'
            rare_items = ''''''
            if users_[str(message.from_user.id)]['user']['rare_items']['have_rare_items']:
                rare_items = '''\n🍀 Редкие предметы:'''
                if users_[str(message.from_user.id)]['user']['rare_items']['ancient_coin']['player_have'] == True: rare_items += '\n - 🪙 Древняя монета'
                if users_[str(message.from_user.id)]['user']['rare_items']['ancient_sword']['player_have'] == True: rare_items += '\n - 🗡 Древний меч'
                if users_[str(message.from_user.id)]['user']['rare_items']['lucky_potion']['player_have'] == True: rare_items += '\n - 🍀 Зелье удачи'
            
            if users_[str(message.from_user.id)]['frog']['is_alive'] == True: alive = 'Лягушка в полном порядке!'
            else: alive = 'Лягушке нужна аптечка'
            await bot.send_message(message.chat.id, 
                            f'''{user_frog}:
<b>Основная информация</b>
🏷 Имя: {users_[str(message.from_user.id)]['frog']['frog_name']}
❤ Здоровье: {alive}
<b>Еда</b>
🍟 Еда для лягушки:
- 🕷 Пауки: {users_[str(message.from_user.id)]['user']['food']['spiders']}
- 🐜 Муравьи: {users_[str(message.from_user.id)]['user']['food']['ants']}
- 🪲 Жуки: {users_[str(message.from_user.id)]['user']['food']['bugs']}
🍪 Сытость: {users_[str(message.from_user.id)]['frog']['frog_satiety']}/10
<b>Валюты</b>
💸 Коины: {users_[str(message.from_user.id)]['user']['money']}
<b>Другое</b>
🎖 Ранг: {ranks_values[str(users_[str(message.from_user.id)]['frog']['rank'])]}{text1} {itemstext} {items}{event_items}{rare_items}''',
                            message_thread_id=message.message_thread_id,
                            parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(message.chat.id, 
                            'У вас нету лягушки!',
                            message_thread_id=message.message_thread_id)

    elif str(message.text).lower() in all_commands['my_balance']:
        logging.info(f'Пользователь {message.from_user.id} посмотрел свой баланс')
        money = users_[str(message.from_user.id)]['user']['money']
        rmoney = round(money)
        await bot.send_message(message.chat.id, 
                        f'Ваш баланс: {rmoney} коинов 💸',
                        message_thread_id=message.message_thread_id)

    elif str(message.text).lower() in all_commands['balance']:
        replym = message.reply_to_message
        idd = replym.from_user.id
        money = users_[str(idd)]['user']['money']
        rmoney = round(money)
        try:
            logging.info(f'Пользователь {message.from_user.id} посмотрел баланс пользователя {idd}')
            await bot.send_message(message.chat.id,
                               f'Баланс данного пользователя: {rmoney}',
                               message_thread_id=message.message_thread_id,
                               reply_to_message_id=replym.message_id)
        except Exception as e:
            logging.error(e)
            await bot.send_message(message.chat.id,
                               f'Баланс данного пользователя: {rmoney}',
                               reply_to_message_id=replym.message_id)