from aiogram import Bot, types
from other.commands import all_commands

async def frog_info_commands(bot: Bot, message: types.Message, users_: dict, config: dict):
    if str(message.text).lower() in all_commands['my_frog']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            print(f'Пользователь {message.from_user.id} посмотрел информацию о своей лягушке')
            if message.from_user.username.lower() in ('', None, '@', 'none'):
                user_frog = f'Ваша лягушка'
            else:
                user_frog = f'Лягушка пользователя <a href="t.me/{message.from_user.username}">{message.from_user.username}</a>'
            ranks_values = {
                '1': 'Деревянный',
                '2': 'Каменный',
                '3': 'Медный',
                '4': 'Бронзовый',
                '5': 'Железный',
                '6': 'Золотой',
                '7': 'Алмазный',
                '8': 'Бриллиантовый',
                '9': 'Премиум ⭐'
            }
            
            text1 = '\n🧵 Предметы'
            items = f''''''
            items_count = 0

            for item in list(users_[str(message.from_user.id)]['frog']['items'].keys()):
                print()
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
🎖 Ранг: {ranks_values[str(users_[str(message.from_user.id)]['frog']['rank'])]}{text1} {itemstext} {items}''',
                            message_thread_id=message.message_thread_id,
                            parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(message.chat.id, 
                            'У вас нету лягушки!',
                            message_thread_id=message.message_thread_id)

    elif str(message.text).lower() in all_commands['my_balance']:
        print(f'Пользователь {message.from_user.id} посмотрел свой баланс')
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
            print(f'Пользователь {message.from_user.id} посмотрел баланс пользователя {idd}')
            await bot.send_message(message.chat.id,
                               f'Баланс данного пользователя: {rmoney}',
                               message_thread_id=message.message_thread_id,
                               reply_to_message_id=replym.message_id)
        except Exception as e:
            print(e)
            await bot.send_message(message.chat.id,
                               f'Баланс данного пользователя: {rmoney}',
                               reply_to_message_id=replym.message_id)