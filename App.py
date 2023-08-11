from telebot.types import InlineKeyboardMarkup as KeyboardMarkup, InlineKeyboardButton as Button
from time import sleep as pause

from random import choice, randint
from other.commands import all_commands
from telebot import TeleBot
from users.save import save_to_json

import datetime as dt

import json

user_start_profile: dict = None

def frog_check(all_users, id):
    if not id in all_users:
        return False
    else:
        return True

with open('config.json', encoding='utf-8') as alll:
    config = json.load(alll)
    
    token = config['token']

with open('users/users.json', encoding='utf-8') as users: users_ = json.load(users)
with open('other/chats.json', encoding='utf-8') as f: chats = json.load(f)
with open('other/items/lucky_coin_level.json', encoding='utf-8') as f: lcl = json.load(f)
with open('other/rank_multiplier.json', encoding='utf-8') as f: rm = json.load(f)

bot = TeleBot(token)

content_types = ('text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact')

@bot.message_handler(content_types=content_types)
def commands(message):
    global user_start_profile
    global chats

    with open('other/user_profile.json', encoding='utf-8') as user_:
        profile = json.load(user_)

    user_start_profile = ({str(message.from_user.id): profile})

    if message.chat.type in ('group', 'supergroup'):
        if message.chat.id not in chats['chats']:
            chats['chats'].append(message.chat.id)

    def has_frog():
        global user_start_profile

        if not str(message.from_user.id) in users_:
            users_.update(user_start_profile)
            hass_frog = False
        else:
            hass_frog = True
        
        if hass_frog == False:
            bot.send_message(message.chat.id, 'У вас нету лягушки!')
    
    has_frog()

    if users_[str(message.from_user.id)]['frog']['frog_satiety'] > 10: users_[str(message.from_user.id)]['frog']['frog_satiety'] = 10
    if users_[str(message.from_user.id)]['frog']['frog_satiety'] < 0: users_[str(message.from_user.id)]['frog']['frog_satiety'] = 0
    if users_[str(message.from_user.id)]['frog']['health'] > 100: users_[str(message.from_user.id)]['frog']['health'] = 100
    if users_[str(message.from_user.id)]['frog']['health'] < 0: users_[str(message.from_user.id)]['frog']['health'] = 0

    # Игнорирование ошибки AttributeError при случае если в сообщении нету текста
    try: message.text.lower()
    except AttributeError: pass

    # Ответ на start
    if str(message.text).lower() in all_commands['start']:

        id_ = str(message.from_user.id)

        if message.from_user.first_name == None: first_name = ''
        else: first_name = ', ' + message.from_user.first_name

        if message.from_user.last_name == None: last_name = ''
        else: last_name = ' ' + message.from_user.last_name

        version = config['version']

        bot.reply_to(message, f'Здравствуйте{first_name}{last_name}. Я - FrogBot. Моя версия - {version}')

    # Ответ на help
    elif str(message.text).lower() in all_commands['help']:
        bot.reply_to(message, '''▶ Старт (/start) - Название и версия бота.
❓ Хелп (/help) - Все команды.
🐸 Взять лягушку (/get_frog) - Взять лягушку.
🍔 Покормить лягушку (/feed_frog) - Покормить лягушку.
🧵 Купить предметы (/buy_items) - Купить предметы для лягушки.
🏷 Дать имя лягушке (/frognameset) - Вы даёте имя лягушке (Имя нужно написать в сообщении после команды).
ℹ Моя лягушка (/my_frog) - Информация о вашей лягушке.
💸 Мой баланс (/my_balance) - Ваш баланс.
⚙️ Отправить лягушку на работу (/send_frog_to_work) - Вы отправляете лягушку на работу.
🔐 Выкупить лягушку из тюрьмы (/buy_frog_out_of_prison) - Если ваша лягушка в тюрьмы, вы можете выкупить её данной командой.
💰 Отправить коины (/send_coins) - Для использования данной команды нужно написать её как ответ на сообщение пользователя которому вы хотите отправить деньги, после текста команды укажите сумму.
💊 Использователь аптечку (/use_first_aid_kit) - Для использования команды нужна 1 аптечка, восстанавливает 20 здоровья.
🤝 Договориться с полицией (/negotiate_with_the_police) - Если ваша лягушка была вором, но вы хотите отправить её на работу полицейским, воспользуйтесь данной командой.''')

    # Ответ на get_frog
    elif str(message.text).lower() in all_commands['get_frog']:
        has_frog()
        
        try: users_[str(message.from_user.id)] = users_[str(message.from_user.id)]
        except KeyError: has_frog()

        now = dt.datetime.now()
        now1 = now.strftime('Час: %H, Минута: %M, Секунда: %S')

        id_ = str(message.from_user.id)

        has_frog = frog_check(users_, id_)

        if has_frog == False:
            bot.send_message(message.chat.id, 'Хей! Вы не зарегистрированы в системе! Если хотите зарегистрироватся напишите "старт"')
        else:
            if users_[id_]['have_frog'] == False:
                bot.send_message(message.chat.id, 'Вы отправились в магазин питомцев, долго рассматривали огромную коллекцую из лягушек! Но наконец, выбрали самую лучшую! Теперь вы друзья! Осталось ей только имя дать!')
                users_[id_]['have_frog'] = True

                save_to_json('users/users', users_)
                
            else:
                bot.send_message(message.chat.id, f'<a href="t.me/{message.from_user.username}">У вас</a> уже есть лягушка.', parse_mode='HTML')


    # Ответ на feed_frog
    elif str(message.text).lower() in all_commands['feed_frog']:
        markup = KeyboardMarkup(row_width=1)

        ant = Button(text='🐜 Муравьём', callback_data='fb_ff_ant')
        spider = Button(text='🕷 Пауком', callback_data='fb_ff_spider')
        bug = Button(text='🪲 Жуком', callback_data='fb_ff_bug')
        
        markup.add(ant, spider, bug)

        bot.reply_to(message, 'Вы решили угостить свою лягушку едой, но какой?', reply_markup=markup)

    # Ответ на команду frog_name_set
    elif tuple(str(str(message.text).lower()).split())[0] in all_commands['give_frog_name_command']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            old_name = users_[str(message.from_user.id)]['frog']['frog_name']

            try: users_[str(message.from_user.id)] = users_[str(message.from_user.id)]
            except KeyError: has_frog()

            message_text_split = message.text.split()
            message_text_split.pop(0)
            name = ' '.join(message_text_split)
            users_[str(message.from_user.id)]['frog']['frog_name'] = name
            name = ' '.join(message_text_split)
            
            if name == old_name:
                bot.reply_to(message, 'Старое имя такое же как новое!')
            else:
                users_[str(message.from_user.id)]['frog']['frog_name'] = name
                bot.reply_to(message, f'Вы успешно изменили имя вашей лягушке 🏷! Старое имя: {old_name}, новое имя: {name} 🐸')     
        else:
            bot.reply_to(message, 'У вас нету лягушки!')
    
    elif tuple(str(str(message.text).lower()).split())[0] in all_commands['give_frog_name_word'] and tuple(str(str(message.text).lower()).split())[1] == 'лягушке' and tuple(str(str(message.text).lower()).split())[2] == 'имя':
        if users_[str(message.from_user.id)]['have_frog'] == True:
            old_name = users_[str(message.from_user.id)]['frog']['frog_name']
            
            try: users_[str(message.from_user.id)] = users_[str(message.from_user.id)]
            except KeyError: has_frog()

            message_text_split = message.text.split()
            
            print(len(message_text_split))
            message_text_split.pop(0)
            message_text_split.pop(0)
            message_text_split.pop(0)
            name = ' '.join(message_text_split)
            
            if name == old_name:
                bot.reply_to(message, 'Старое имя такое же как новое!')
            else:
                users_[str(message.from_user.id)]['frog']['frog_name'] = name
                bot.reply_to(message, f'Вы успешно изменили имя вашей лягушке  🏷! Старое имя: {old_name}, новое имя: {name} 🐸')
        else:
            bot.reply_to(message, 'У вас нету лягушки!')
    
    # Ответ на команду my_frog
    elif str(message.text).lower() in all_commands['my_frog']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            try: users_[str(message.from_user.id)] = users_[str(message.from_user.id)]
            except KeyError: has_frog()

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

            
            items = f''''''
            items_count = 0

            if users_[str(message.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                level = users_[str(message.from_user.id)]['frog']['items']['lucky_coin']['level']
                items = items.join(f'\n - 🍀 Коин удачи {level} уровня')
                items_count += 1
            
            if items == f'''''':
                items = '\n    Нет'

            bot.reply_to(message, f'''{user_frog}:
🏷 Имя: {users_[str(message.from_user.id)]['frog']['frog_name']}
❤ Здоровье: {users_[str(message.from_user.id)]['frog']['health']}
🍪 Сыстость: {users_[str(message.from_user.id)]['frog']['frog_satiety']}/10
😁 Настроение: {users_[str(message.from_user.id)]['frog']['frog_happines_level']}/100
💸 Коины: {users_[str(message.from_user.id)]['user']['money']}
🍟 Еда для лягушки:
 - 🕷 Пауки: {users_[str(message.from_user.id)]['user']['food']['spiders']}
 - 🐜 Муравьи: {users_[str(message.from_user.id)]['user']['food']['ants']}
 - 🪲 Жуки: {users_[str(message.from_user.id)]['user']['food']['bugs']}
🎖 Ранг: {ranks_values[str(users_[str(message.from_user.id)]['frog']['rank'])]}
🧵 Предметы ({items_count}): {items}''', parse_mode="HTML")
        else:
            bot.reply_to(message, 'У вас нету лягушки!')

    # Ответ на команду send_frog_to_work
    elif str(message.text).lower() in all_commands['send_frog_to_work']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            markup = KeyboardMarkup(row_width=1)

            tips = [
                'Советуем вам не отправлять лягушку на работу грабителем, пока у вас не будет примерно 1500 коинов.', 
                'Работа полицейским - прибыльнее вора. Но, если станешь вором - не сможешь стать полицейским!',
                'Уборщик - единственная работа где есть 1 вариант развития событий рабочего дня.',
                'Повар - работа с самым большим количеством вариантов развития событий.',
                'До 0.0.5 была только одна работа - офисный работник.',
                'Офисный работник - самая плохая работа из всех, ведь на ней мало платят, и большой шанс что ваша лягушка сбежит с работы.',
                'Уборщик - лучшая работа для новичков, на ней мало платят, но всегда!',
                'В обновлении 0.0.6 добавили целых 3 работы!',
                'Раньше рабочий день лягушки длился 10 секунд.',
                'До обновления 0.0.6 шанс ограбить что-то за вора был 20%, после - 30%',
                'Вы не можете отправить лягушку на работу два раза в один момент.'
            ]

            tip = choice(tips)

            office_worker = Button(text='📄 Лягушка будет офисным работником!', callback_data='fb_w_office_worker')
            criminal = Button(text='🔪 Лягушка будет преступником!', callback_data='fb_w_criminal')
            police = Button(text='👮‍♂️ Лягушка будет полицейским!', callback_data='fb_w_police')
            cleaner = Button(text='🧹 Лягушка будет уборщиком!', callback_data='fb_w_cleaner')
            cook = Button(text='👨‍🍳 Лягушка будет поваром!', callback_data='fb_w_cook')
            programmer = Button(text='👨‍💻 Лягушка будет программистом!', callback_data='fb_w_programmer')

            markup.add(office_worker, criminal, police, cleaner, cook, programmer)

            bot.reply_to(message, f'''Наконец, вы решили отправить свою лягушку на работу! Перед вами выбор, сделать свою лягушку нарушителем закона, или честным офисным работником?

ℹ {tip}''',
            reply_markup=markup)
    
    # Ответ на команду my_balance
    elif str(message.text).lower() in all_commands['my_balance']:
        money = users_[str(message.from_user.id)]['user']['money']
        bot.reply_to(message, f'Ваш баланс: {money} коинов 💸')
    
    # Ответ на команду buy_food
    elif str(message.text).lower() in all_commands['buy_items']:
        markup = KeyboardMarkup(row_width=2)
        
        food = Button(text='🥞 Еду', callback_data='fb_b_food')
        first_aid_kit = Button(text='💊 Аптечки', callback_data='fb_b_first_aid_kit')
        lucky_coin = Button(text='🍀 Коин удачи', callback_data='fb_b_lucky_coin')

        markup.add(first_aid_kit, food, lucky_coin)

        bot.reply_to(message, 'Вы отправились в магазин предметов, но, что вы хотите купить?', reply_markup=markup)
    
    elif str(message.text).lower() in all_commands['buy_frog_out_of_prison']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            if users_[str(message.from_user.id)]['frog']['frog_in_jail'] == True:
                if users_[str(message.from_user.id)]['user']['money'] >= 325:
                    users_[str(message.from_user.id)]['frog']['frog_in_jail'] = False
                    users_[str(message.from_user.id)]['user']['money'] -= 325
                    bot.reply_to(message, 'Вы успешно выкупили лягушку из тюрьмы 🐸')
                else:
                    bot.reply_to('''У вас недостаточно средств для выкупа лягушки из тюрьмы.
Необходимая сума: 325 коинов 💵''')
            else:
                bot.reply_to(message, 'Ваша лягушка на свободе 🐸')
        else:
            bot.reply_to(message, 'У вас нету лягушки!')
    
    elif str(message.text).lower() in all_commands['rassilka'] and message.from_user.id == 2006262756:
        with open('txt.txt', encoding='utf-8') as f:
            txt = f.read()
        for i in chats['chats']:
            bot.send_message(i, txt, parse_mode='HTML')
    
    elif str(message.text).lower().split()[0] in all_commands['send_money']:
        if len(str(message.text).lower().split()) == 2:
            msgrtmsg = message.reply_to_message

            send = int(''.join(str(message.text).lower().split().pop(1)))

            if msgrtmsg:
                if users_[str(message.from_user.id)]['user']['money'] >= send:
                    users_[str(message.from_user.id)]['user']['money'] -= send
                    users_[str(msgrtmsg.from_user.id)]['user']['money'] += send
                    bot.reply_to(message, 'Вы успешно отправили коины 💳')
                else:
                    bot.reply_to(message, 'Недостаточно средств для совершения операции перевода 💸')
            else:
                bot.reply_to(message, 'Для того, чтобы отправить коины, вам нужно написать сообщение ввиде ответа на сообщение пользователя, которому вы хотите перевести коины 💰')
        else:
            bot.reply_to(message, 'Введите сумму коинов после команды')
    
    if len(str(message.text).lower().split()) == 3:
        txt = ''.join(str(message.text).lower().split().pop(0))
        txt2 = ''.join(str(message.text).lower().split().pop(1))
        txt3 = txt + ' ' + txt2
        if txt3 in all_commands['send_money_2_words']:
            msgrtmsg = message.reply_to_message

            listt = str(message.text).lower().split().pop(2)
                    
            send = int(''.join(listt))

            if msgrtmsg:
                if users_[str(message.from_user.id)]['user']['money'] >= send:
                    users_[str(message.from_user.id)]['user']['money'] -= send
                    users_[str(msgrtmsg.from_user.id)]['user']['money'] += send
                    bot.reply_to(message, 'Вы успешно отправили коины 💳')
                else:
                    bot.reply_to(message, 'Недостаточно средств для совершения операции перевода 💸')
            else:
                bot.reply_to(message, 'Для того, чтобы отправить коины, вам нужно написать сообщение ввиде ответа на сообщение пользователя, которому вы хотите перевести коины 💰')
    

    if str(message.text).lower() in all_commands['use_first_aid_kit']:
        if users_[str(message.from_user.id)]['user']['first_aid_kits'] > 0:
            if users_[str(message.from_user.id)]['frog']['health'] < 100:
                users_[str(message.from_user.id)]['user']['first_aid_kits'] -= 1
                users_[str(message.from_user.id)]['frog']['health'] += 20
                bot.reply_to(message, 'Вы успешно восстановили здоровье своей лягушке ❤!')
            else:
                bot.reply_to(message, 'У вашей лягушки полное здоровье ❤')
        else:
            bot.reply_to(message, 'У вас нету аптечек!')
    
    if str(message.text).lower() in all_commands['negotiate_with_the_police']:
        markup = KeyboardMarkup(row_width=3)

        coins300 = Button(text='💲 300 Коинов', callback_data='fb_nwtp_300c')
        coins500 = Button(text='💵 500 Коинов', callback_data='fb_nwtp_500c')
        coins750 = Button(text='💰 750 коинов', callback_data='fb_nwtp_750c')

        markup.add(coins300, coins500, coins750)

        bot.reply_to(message, 'Вы решили договориться с полицией насчёт работы вашей лягушки грабителем. Сколько вы заплатите им?', reply_markup=markup)

    if str(message.text).lower() in all_commands['upgrade']:
        markup = KeyboardMarkup(row_width=2)

        rank = Button(text='🎖 Ранг', callback_data='fb_u_rank')
        item = Button(text='🧵 Предмет', callback_data='fb_u_item')

        markup.add(rank, item)

        bot.reply_to(message, 'Вы хотите улучшить что-то, но что?', reply_markup=markup)

    save_to_json('users/users', users_)
    save_to_json('other/chats', chats)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global lcl
    global rm

    if call.data == 'fb_w_criminal':
        markup = KeyboardMarkup(row_width=1)

        thief = Button(text='🔓 Лягушка будет вором!', callback_data='fb_w_c_thief')
        killer = Button(text='🔪 Лягушка будет убийцей!', callback_data='fb_w_c_killer')
        hacker = Button(text='👨‍💻 Лягушка будет хакером!', callback_data='fb_w_hacker')

        markup.add(thief, killer, hacker)

        bot.reply_to(call.message, 'Вы решили что ваша лягушка будет преступником. Но преступником какого рода? 🤔', reply_markup=markup)
    
    if call.data == 'fb_w_programmer':
        markup = KeyboardMarkup(row_width=1)

        programmer = Button(text='💻 Лягушка будет честным программистом!', callback_data='fb_w_p_programmer')
        hacker = Button(text='👨‍💻 Лягушка будет хакером!', callback_data='fb_w_hacker')

        markup.add(programmer, hacker)

        bot.reply_to(call.message, 'Лягушка будет программистом. Но каким? 🤔', reply_markup=markup)
    
    if call.data == 'fb_w_hacker':
        markup = KeyboardMarkup(row_width=1)

        white_hacker = Button(text='💻 Лягушка будет белым хакером!', callback_data='fb_w_h_white_hacker')
        hacker = Button(text='👨‍💻 Лягушка будет хакером!', callback_data='fb_w_h_hacker')

        markup.add(hacker, white_hacker)

        bot.reply_to(call.message, 'Вы решили что лягушка будет хакером. Но каким? 🤔', reply_markup=markup)

    if call.data == 'fb_w_office_worker':
        if users_[str(call.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(call.from_user.id)]['frog']['frog_satiety'] >= 1:
                if users_[str(call.from_user.id)]['frog']['frog_in_jail'] == False:
                    bot.reply_to(call.message, '''Вы успешно отправили вашу лягушку на работу офисным работником 🐸! Пожелайте ей удачи 🍀!

🕔 Информация о том, как прошёл рабочий день придёт через 3 минуты.''')
                    
                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = True

                    results = ('successful', 'error', 'escape')

                    result = choice(results)
                    pause(180)

                    users_[str(call.from_user.id)]['frog']['frog_satiety'] -= 1

                    if result == 'successful':
                        what_frog_do = choice(('составляя отчёты', 'настраивая программы клиентам'))
                        add = randint(100, 175)
                        print(add)
                        if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                            add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                            add = round(add)
                        print(add)
                        add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                        print(add)
                        users_[str(call.from_user.id)]['user']['money'] += add
                        text = f'''Ваша лягушка успешно провела рабочий день {what_frog_do}.
Вы получили:
 - 💵 {add} коинов'''

                    elif result == 'error':
                        text = 'О нет! Ваша лягушка совершила ошибку и её уволили! Вы ничего не получили!'
                    elif result == 'escape':
                        text = 'Ваша лягушка решила сбежать с работы... И у неё получилось! Вы ничего не получили.'

                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = False

                    bot.reply_to(call.message, text)
            
                else:
                    bot.reply_to(call.message, 'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!')
        
            else:
                bot.reply_to(call.message, 'Ваша лягушка не может работать пока голодна 🦴!')
        
        else:
            bot.reply_to(call.message, 'Ваша лягушка уже на работе!')

    elif call.data == 'fb_w_c_thief':
        if users_[str(call.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(call.from_user.id)]['frog']['frog_satiety'] >= 1:
                if users_[str(call.from_user.id)]['frog']['frog_in_jail'] == False:
                    users_[str(call.from_user.id)]['frog']['has_been_thief'] = True

                    bot.reply_to(call.message, '''🔑 Вы успешно отправили вашу лягушку на работу грабителем! Вы сошли с ума?! Она же может попасть в тюрьму!

🕔 Сообщение о результате ограбления придёт через 3 минуты.''')
                    
                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = True

                    results = ('successful', 'successful', 'successful', 'cops', 'cops', 'cops', 'cops', 'cops', 'cops', 'cops')

                    result = choice(results)
                    pause(180)

                    users_[str(call.from_user.id)]['frog']['frog_satiety'] -= 1

                    if result == 'successful':
                        what_frog_robbed = choice(('аптеку', 'аптеку', 'аптеку', 'музей', 'музей', 'музей', 'дом', 'дом', 'дом', 'дом', 'банк'))
                        if what_frog_robbed == 'аптеку': add = randint(225, 290)
                        if what_frog_robbed == 'дом': add = randint(150, 375)
                        if what_frog_robbed == 'банк': add = randint(375, 500)
                        if what_frog_robbed == 'музей': add = randint(475, 550)
                        print(add)
                        if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                            add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                            add = round(add)
                        print(add)
                        add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                        print(add)
                        users_[str(call.from_user.id)]['user']['money'] += add
                        text = f'''Ваша лягушка успешно ограбила {what_frog_robbed}.
Вы получили:
 - 💵 {add} коинов'''

                    elif result == 'cops':
                        users_[str(call.from_user.id)]['frog']['frog_in_jail'] = True
                        users_[str(call.from_user.id)]['frog']['has_been_in_jail'] = True
                        users_[str(call.from_user.id)]['frog']['can_be_cop_after_thief'] = False
                        text = 'О нет! Ваша лягушка попалась полиции и её посадили в тюрьму! 😱'
                    
                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = False

                    bot.reply_to(call.message, text)
                else:
                    bot.reply_to(call.message, 'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!')

            else:
                bot.reply_to(call.message, 'Ваша лягушка не может работать пока голодна 🦴!')

        else:
            bot.reply_to(call.message, 'Ваша лягушка уже на работе!')

    if call.data == 'fb_w_police':
        if users_[str(call.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(call.from_user.id)]['frog']['health'] >= 20:
                if users_[str(call.from_user.id)]['frog']['frog_satiety'] >= 1:
                    if users_[str(call.from_user.id)]['frog']['frog_in_jail'] == False:
                        if users_[str(call.from_user.id)]['frog']['can_be_cop_after_thief'] == True:
                            bot.reply_to(call.message, '''Вы успешно отправили вашу лягушку на работу полицейским 👮‍♂️! Пожелайте ей удачи 🍀!

🕔 Информация о том, как прошёл рабочий день придёт через 3 минуты.''')
                            
                            users_[str(call.from_user.id)]['frog']['frog_on_work'] = True

                            results = ('normal_day', 'fail', 'fail', 'fail', 'fail', 'killer', 'thief', 'thief', 'thief', 'thief')

                            result = choice(results)
                            pause(180)

                            users_[str(call.from_user.id)]['frog']['frog_satiety'] -= 1

                            def give_money_count(min_, max_, tmin, tmax):
                                global users_
                                if users_[str(call.from_user.id)]['frog']['has_been_in_jail'] == True: ad = randint(tmin, tmax)
                                else: ad = randint(min_, max_)
                                print(ad)
                                if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                                    ad *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                                    ad = round(ad)
                                print(ad)
                                ad *= rm[str(users_[str(call.from_user.id)]['frog']['rank'])]
                                print(ad)
                                return ad

                            if result == 'normal_day':
                                add = give_money_count(55, 138, 23, 54)
                                users_[str(call.from_user.id)]['user']['money'] += add
                                print(add)
                                text = f'''Ваша лягушка никого не арестовала, ей заплатили копейки.
Вы получили:
 - 💵 {add} коинов'''

                            elif result == 'killer':
                                add = give_money_count(600, 700, 300, 350)
                                users_[str(call.from_user.id)]['user']['money'] += add
                                print(add)
                                text = f'''Ого! Ваша лягушка арестовала убийцу! Ей заплатили очень много коинов!
Вы получили:
 - 💵 {add} коинов'''
                    
                            elif result == 'thief':
                                where = choice(['доме', 'аптеке', 'музее', 'банке'])
                                if where == 'доме': add = give_money_count(200, 368, 100, 134)
                                elif where == 'аптеке': add = give_money_count(350, 400, 175, 200)
                                elif where == 'музее': add = give_money_count(450, 500, 275, 350)
                                elif where == 'банке': add = give_money_count(400, 550, 200, 275)
                                users_[str(call.from_user.id)]['user']['money'] += add
                                print(add)
                                text = f'''Ваша лягушка арестовала вора в {where}! Ей заплатили много коинов!
Вы получили:
 - 💵 {add} коинов'''

                            elif result == 'fail':
                                add = give_money_count(255, 355, 255, 355)
                                users_[str(call.from_user.id)]['user']['money'] += add
                                users_[str(call.from_user.id)]['frog']['health'] -= 20
                                print(add)
                                text = f'''Ваша лягушка попыталась арестовать опасного грабителя, но он отбился и убежал. Но, вам дали коинов за храбрость вашей лягушки 👍
Вы получили:
 - 💵 {add} коинов
Вы потеряли:
 - ❤ 20 здоровья'''
                            users_[str(call.from_user.id)]['frog']['frog_on_work'] = False

                            bot.reply_to(call.message, text)

                        else:
                            bot.reply_to(call.message, 'Ваша лягушка когда-то была преступником 🔒! Вы не можете отправить её на работу полицейским ❌!')                    

                    else:
                        bot.reply_to(call.message, 'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!')

                else:
                    bot.reply_to(call.message, 'Ваша лягушка не может работать пока голодна 🦴!')
            
            else:
                bot.reply_to(call.message, 'У вашей лягушки мало здоровья для работы, сначала вылечите её ❤!')
        
        else:
            bot.reply_to(call.message, 'Ваша лягушка уже на работе!')

    elif call.data == 'fb_w_cleaner':
        if users_[str(call.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(call.from_user.id)]['frog']['frog_satiety'] >= 1:
                if users_[str(call.from_user.id)]['frog']['frog_in_jail'] == False:

                    bot.reply_to(call.message, '''Вы успешно отправили вашу лягушку на работу уборщиком 🧹!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.''')
                    
                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = True

                    pause(180)

                    users_[str(call.from_user.id)]['frog']['frog_satiety'] -= 1
                    add = randint(50, 75)
                    print(add)
                    if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                        add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                        add = round(add)
                    print(add)
                    add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                    print(add)
                    users_[str(call.from_user.id)]['user']['money'] += add
                    text = f'''Ваша лягушка провела рабочий день уборщиком, ей заплатили копейки.
Вы получили:
 - 💵 {add} коинов'''

                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = False

                    bot.reply_to(call.message, text)
                else:
                    bot.reply_to(call.message, 'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!')
        
            else:
                bot.reply_to(call.message, 'Ваша лягушка не может работать пока голодна 🦴!')

        else:
            bot.reply_to(call.message, 'Ваша лягушка уже на работе!')

    elif call.data == 'fb_w_cook':
        if users_[str(call.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(call.from_user.id)]['frog']['frog_satiety'] >= 1:
                if users_[str(call.from_user.id)]['frog']['frog_in_jail'] == False:

                    bot.reply_to(call.message, '''Вы успешно отправили вашу лягушку на работу поваром 👨‍🍳!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.''')
                    
                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = True

                    pause(180)

                    results = (
                        'успешно',
                        'успешно',
                        'успешно',
                        'недожарилась',
                        'недожарилась',
                        'недожарилась',
                        'подгорела',
                        'сгорела',
                        'сгорела',
                        'просрочка'
                    )

                    result = choice(results)

                    users_[str(call.from_user.id)]['frog']['frog_satiety'] -= 1

                    if result == 'успешно':
                        add = randint(100, 275)
                        print(add)
                        if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                            add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                            add = round(add)
                        print(add)
                        add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                        print(add)
                        users_[str(call.from_user.id)]['user']['money'] += add
                        text = f'''Ваша лягушка успешно приготовила блюдо.
Вы получили:
 - 💵 {add} коинов'''
                
                    elif result == 'недожарилась':
                        client = choice(['заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'не заметил', 'не заметил', 'не заметил', 'не заметил'])
                        if client == 'заметил':
                            text = 'Ваша лягушка недожарила блюдо, клиент это заметил и её уволили.'
                        elif client == 'не заметил':
                            add = randint(50, 175)
                            print(add)
                            if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                                add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                                add = round(add)
                            print(add)
                            add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                            print(add)
                            users_[str(call.from_user.id)]['user']['money'] += add
                            text = f'''Ваша лягушка недожарила блюдо, клиент этого не заметил, но вам заплатили меньше.
Вы получили:
 - 💵 {add} коинов'''
                
                    elif result == 'подгорела':
                        client = choice(['заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'не заметил', 'не заметил'])
                        if client == 'заметил':
                            text = 'Блюдо вашей лягушки подгорело, клиент это заметил и её уволили'
                        elif result == 'не заметил':
                            add = randint(25, 100)
                            print(add)
                            if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                                add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                                add = round(add)
                            print(add)
                            add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                            print(add)
                            users_[str(call.from_user.id)]['user']['money'] += add
                            text = f'''У вашей лягушки подгорело блюдо, клиент этого не заметил, но вам заплатили меньше.
Вы получили:
 - 💵 {add} коинов'''
                
                    elif result == 'сгорела':
                        text = 'Блюдо вашей лягушки сгорело, её уволили'
                
                    elif result == 'просрочка':
                        text = 'Ваша лягушка приготовила блюдо из просрочки, её уволили'

                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = False

                    bot.reply_to(call.message, text)
            else:
                bot.reply_to(call.message, 'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!')
        
        else:
            bot.reply_to(call.message, 'Ваша лягушка не может работать пока голодна 🦴!')
    
    elif call.data == 'fb_w_c_killer':
        if users_[str(call.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(call.from_user.id)]['frog']['frog_satiety'] >= 1:
                if users_[str(call.from_user.id)]['frog']['frog_in_jail'] == False:
                    bot.reply_to(call.message, '''Вы успешно отправили вашу лягушку на работу киллером 🔪!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.''')
                    
                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = True

                    pause(180)

                    results = (
                        'успешно',
                        'провал',
                        'провал',
                        'провал',
                        'провал',
                        'провал',
                        'провал',
                        'провал',
                        'провал',
                        'провал',
                    )

                    result = choice(results)

                    users_[str(call.from_user.id)]['frog']['frog_satiety'] -= 1

                    if result == 'провал':
                        users_[str(call.from_user.id)]['frog']['frog_in_jail'] = True
                        users_[str(call.from_user.id)]['frog']['has_been_in_jail'] = True
                        users_[str(call.from_user.id)]['frog']['can_be_cop_after_thief'] = False
                        text = 'О нет! Ваша лягушка попалась полиции и её посадили в тюрьму! 😱'
                    if result == 'успешно':
                        add = randint(900, 1100)
                        print(add)
                        if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
                            add *= lcl[str(users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                            add = round(add)
                        print(add)
                        add *= int(round(rm[str(users_[str(call.from_user.id)]['frog']['rank'])]))
                        print(add)
                        users_[str(call.from_user.id)]['user']['money'] += add
                        text = f'''Ваша лягушка успешно убила другую лягушку.
Вы получили:
 - 💵 {add} коинов'''

                    users_[str(call.from_user.id)]['frog']['frog_on_work'] = False

                    bot.reply_to(call.message, text)

    
    if call.data == 'fb_b_first_aid_kit':
        if users_[str(call.from_user.id)]['user']['money'] >= 100:
            users_[str(call.from_user.id)]['user']['first_aid_kits'] += 1
            users_[str(call.from_user.id)]['user']['money'] -= 100
            bot.reply_to(call.message, 'Вы успешно купили аптечку!')
        else:
            bot.reply_to(call.message, '''Недостаточно средств для совершения операции покупки аптечки!
Необходимая сумма: 100 коинов 💸''')
    
    if call.data == 'fb_b_food':
        markup = KeyboardMarkup(row_width=1)

        spider = Button(text='🕷 Я хочу купить паука', callback_data='fb_b_f_spider')
        bug = Button(text='🪲 Я хочу купить жука', callback_data='fb_b_f_bug')
        ant = Button(text='🐜 Я хочу купить муравья', callback_data='fb_b_f_ant')

        markup.add(spider, bug, ant)

        bot.reply_to(call.message, 'Итак, вы решили купить еду лягушке, но какую? 🐜', reply_markup=markup)

    def buy_food(cost, type_, type_msg):
        global users_
        if users_[str(call.from_user.id)]['user']['money'] >= cost:
            users_[str(call.from_user.id)]['user']['money'] -= cost
            users_[str(call.from_user.id)]['user']['food'][type_] += 1
            bot.reply_to(call.message, f'Вы успешно купили {type_msg} для своей лягушки 🐸!')
        else:
            bot.reply_to(call.message, f'''Недостаточно средств для совершения операции покупки {type_msg}!
Необходимая сумма: {cost} коинов 💸''')

    if call.data == 'fb_b_f_spider':
        buy_food(150, 'spiders', 'паука')

    if call.data == 'fb_b_f_bug':
        buy_food(100, 'bugs', 'жука')

    if call.data == 'fb_b_f_ant':
        buy_food(50, 'ants', 'муравья')
    
    def feed_frog(satiety, type_, type_msg, emoji, type_msgg):
        global users_
        if users_[str(call.from_user.id)]['frog']['frog_satiety'] < 10:
            if users_[str(call.from_user.id)]['user']['food'][type_] > 0:
                users_[str(call.from_user.id)]['frog']['frog_satiety'] += satiety
                users_[str(call.from_user.id)]['user']['food'][type_] -= 1
                bot.reply_to(call.message, f'Вы успешно накормили свою лягушку {type_msg} {emoji}!')
            else:
                bot.reply_to(call.message, f'У вас нету ни одного {type_msgg} {emoji}!')
        else:
            bot.reply_to(call.message, 'Ваша лягушка сыта 🍟!')

    if call.data == 'fb_ff_ant':
        feed_frog(1, 'ants', 'муравьём', '🐜', 'муравья')
    if call.data == 'fb_ff_spider':
        feed_frog(3, 'spiders', 'пауком', '🕷', 'паука')
    if call.data == 'fb_ff_bug':
        feed_frog(2, 'bugs', 'жуком', '🪲', 'жука')
    
    def negotiate(userid, coinsc, chatid, results):
        global users_
        
        if users_[str(userid)]['frog']['can_be_cop_after_thief'] == False:
            if users_[str(userid)]['user']['money'] >= coinsc:
                users_[str(call.from_user.id)]['user']['money'] -= coinsc
                
                result = choice(results)

                if result == 'fail':
                    bot.send_message(chatid, 'Вы не смогли договориться с полицией, вы просто потратили свои коины.')
                else:
                    bot.send_message(chatid, 'Вы успешно договорились с полицией, теперь ваша лягушка может работать полицейским, хоть и с зарплатой в 2 раза меньше!')
                    users_[str(userid)]['frog']['can_be_cop_after_thief'] = True
            else:
                bot.send_message(chatid, 'У вас недостаточно коинов!')
        else:
            bot.send_message(chatid, 'Ваша лягушка уже может работать полицейским')
    
    if call.data == "fb_nwtp_300c":
        negotiate(call.from_user.id, 300, call.message.chat.id, [
            'fail', 'fail', 'fail', 'fail', 'fail', 'fail', 'fail',
            'good', 'good', 'good'
        ])

    if call.data == "fb_nwtp_500c":
        negotiate(call.from_user.id, 500, call.message.chat.id, [
            'fail', 'fail', 'fail', 'fail', 'fail',
            'good', 'good', 'good', 'good', 'good'
        ])
    
    if call.data == "fb_nwtp_750c":
        negotiate(call.from_user.id, 750, call.message.chat.id, [
            'fail', 'fail', 'fail',
            'good', 'good', 'good', 'good', 'good', 'good', 'good'
        ])
    
    if call.data == 'fb_u_item':
        markup = KeyboardMarkup(row_width=1)

        if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['has_lucky_coin'] == True:
            markup.add(Button(text='🍀 Коин удачи', callback_data='fb_u_i_lucky_coin'))

        bot.reply_to(call.message, 'Вы решили улучшить предмет, но какой?', reply_markup=markup)
    
    if call.data == 'fb_u_i_lucky_coin':
        if users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'] < 3:
            level_costs = {
                "2": 1000,
                "3": 2500
            }
            blevel = users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'] + 1
            if users_[str(call.from_user.id)]['user']['money'] >= level_costs[str(blevel)]:
                users_[str(call.from_user.id)]['user']['money'] -= level_costs[str(blevel)]
                users_[str(call.from_user.id)]['frog']['items']['lucky_coin']['level'] += 1
                bot.reply_to(call.message, 'Вы успешно улучшили ваш предмет!')
        else:
            bot.reply_to(call.message, 'У вашего предмета максимальный уровень!')
    
    if call.data == 'fb_u_rank':
        if users_[str(call.from_user.id)]['frog']['rank'] < 8:
            cost = {
                '2': 5000,
                '3': 7500,
                '4': 10000,
                '5': 12500,
                '6': 15000,
                '7': 17500,
                '8': 20000
            }
            ranks_values = {
                '1': 'Деревянный',
                '2': 'Каменный',
                '3': 'Медный',
                '4': 'Бронзовый',
                '5': 'Железный',
                '6': 'Золотой',
                '7': 'Алмазный',
                '8': 'Бриллиантовый'
            }

            brank = users_[str(call.from_user.id)]['frog']['rank'] + 1
            befrank = users_[str(call.from_user.id)]['frog']['rank']

            if users_[str(call.from_user.id)]['user']['money'] >= cost[str(brank)]:
                users_[str(call.from_user.id)]['user']['money'] -= cost[str(brank)]
                users_[str(call.from_user.id)]['frog']['rank'] += 1
                rankn = users_[str(call.from_user.id)]['frog']['rank']
                bot.reply_to(call.message, f'Вы успешно повысили свой ранг! Ваш прошлый ранг: {ranks_values[str(befrank)]}, ваш текущий ранг: {ranks_values[str(rankn)]}')
            else:
                bot.reply_to(call.message, f'У вас недостаточно монет! Необходимая сумма: {cost[brank]}.')
        else:
            bot.reply_to(call.message, 'У вас максимальный бесплатный ранг\! ||Да, максимальный __бесплатный__ ранг, у нас скоро будет донат 😉||', parse_mode='MarkdownV2')
            

    save_to_json('users/users', users_)


print('Я запустился!')

bot.polling(none_stop=True)