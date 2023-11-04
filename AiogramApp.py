# Aiogram import | Импортирование Aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup as KMarkup, InlineKeyboardButton as Button

# Other imports | Другие импорты
from random import choice, randint
from asyncio import sleep
from colorama import init, Fore
import json
import logging

# Custom scripts imports | Импорты кастомных скриптов
from users.save import save_to_json
from scripts.fb_ff import *
from scripts.change_name import *
from scripts.frog_info import *
from scripts.not_frog_commands import *
from scripts.main_commands import *
from scripts.work_commands import *
from scripts.admin_commands import *
from utilities.work import *
from scripts.cases import *
from scripts.buy_food import *

init(autoreset=True)

with open('config.json', encoding='utf-8') as alll:
    config = json.load(alll)
    
    token = config['token']

with open('users/users.json', encoding='utf-8') as users: users_ = json.load(users)
with open('other/chats.json', encoding='utf-8') as f: chats = json.load(f)

bot = Bot(token=token)
dp = Dispatcher(bot)

blue = Fore.BLUE
yellow = Fore.YELLOW
cyan = Fore.CYAN

# Команды
@dp.message_handler()
async def messages(message: types.Message):
    await not_frog(bot, message, users_)
    await main(bot, message, users_)
    await work(bot, message, users_, config)
    await frog_info_commands(bot, message, users_, config)
    await admin(bot, message, users_, config)
    await open_case(bot, message, users_, config)

    save_to_json('users/users.json', users_)
    save_to_json('other/chats.json', chats)

# Feeding frog | Кормим лягушку
# Ant | Муравей
@dp.callback_query_handler(text = 'fb_ff_ant')
async def ff_ant(callback: types.CallbackQuery):
    await fb_ff(callback, bot, users_, 1, 'ants')
    print(f'{yellow}Пользователь {callback.from_user.id} покормил лягушку муравьём')
# Spider | Паук
@dp.callback_query_handler(text = 'fb_ff_spider')
async def ff_spider(callback: types.CallbackQuery):
    await fb_ff(callback, bot, users_, 3, 'spiders')
    print(f'{yellow}Пользователь {callback.from_user.id} покормил лягушку пауком')
# Bug | Жук
@dp.callback_query_handler(text = 'fb_ff_bug')
async def ff_bug(callback: types.CallbackQuery):
    await fb_ff(callback, bot, users_, 2, 'bugs')
    print(f'{yellow}Пользователь {callback.from_user.id} покормил лягушку жуком')

# Negotiate with the police | Договор с полицией
# 300 coins
@dp.callback_query_handler(text = 'fb_nwtp_300c')
async def ff_bug(callback: types.CallbackQuery):
    await negotiate(bot, callback.message, users_, 300, callback)
    print(f'{cyan}Пользователь {callback.from_user.id} попытался договориться с полицией за 300 коинов')
# 500 coins
@dp.callback_query_handler(text = 'fb_nwtp_500c')
async def ff_bug(callback: types.CallbackQuery):
    await negotiate(bot, callback.message, users_, 500, callback)
    print(f'{cyan}Пользователь {callback.from_user.id} попытался договориться с полицией за 500 коинов')
# 750 coins
@dp.callback_query_handler(text = 'fb_nwtp_750c')
async def ff_bug(callback: types.CallbackQuery):
    await negotiate(bot, callback.message, users_, 750, callback)
    print(f'{cyan}Пользователь {callback.from_user.id} попытался договориться с полицией за 750 коинов')

@dp.callback_query_handler(text = 'fb_w_office_worker')
async def office_worker(callback: types.CallbackQuery):
    message = callback.message
    if users_[str(callback.from_user.id)]['frog']['frog_on_work'] == False:
        if users_[str(callback.from_user.id)]['frog']['frog_satiety'] >= 1:
            if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
                print(f'Пользователь {callback.from_user.id} отправил лягушку на работу офисным работником')
                await bot.send_message(message.chat.id, 
                                 '''Вы успешно отправили вашу лягушку на работу офисным работником 🐸! Пожелайте ей удачи 🍀!

🕔 Информация о том, как прошёл рабочий день придёт через 3 минуты.''',
                                 message_thread_id=message.message_thread_id)
                    
                users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True
                results = ('successful', 'successful', 'successful', 'error', 'escape')
                result = choice(results)
                await sleep(180)
                users_[str(callback.from_user.id)]['frog']['frog_satiety'] -= 1
                if result == 'successful':
                    print(f'Лягушка пользователя {callback.from_user.id} успешно провела рабочий день офисным работником.')
                    what_frog_do = choice(('составляя отчёты', 'настраивая программы клиентам'))
                    add = randint(100, 175)
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
                        addd = add * config['items_i']['lucky_coin'][str(users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                        addd -= add
                        addd = round(addd)
                        users_[str(callback.from_user.id)]['user']['money'] += addd
                    if users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['player_has'] == True:
                        addd = add * config['items_i']['magic_diamond'][str(users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['level'])]
                        addd -= add
                        addd = round(addd)
                        users_[str(callback.from_user.id)]['user']['money'] += addd

                    if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
                        add_r = add * int(round(config['rank_multiplier'][str(users_[str(callback.from_user.id)]['frog']['rank'])]))
                        users_[str(callback.from_user.id)]['user']['money'] += add_r
                    users_[str(callback.from_user.id)]['user']['money'] += add
                    text = f'''Ваша лягушка успешно провела рабочий день {what_frog_do}.
Вы получили:
 - 💵 {add} коинов'''
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True or users_[str(callback.from_user.id)]['frog']['rank'] != 1:
                        text += '\nБонусы:'
                    if addd != 0:
                        text += f'\n - 💵 {addd} коинов (Предметы)'
                    if add_r != 0:
                        text += f'\n - 💵 {add_r} коинов (Ранг)'

                elif result == 'error':
                    print(f'Лягушка пользователя {callback.from_user.id} совершила ошибку на работе офисным работником')
                    text = 'О нет! Ваша лягушка совершила ошибку и её уволили! Вы ничего не получили!'
                elif result == 'escape':
                    print(f'Лягушка пользователя {callback.from_user.id} сбежала с работы')
                    text = 'Ваша лягушка решила сбежать с работы... И у неё получилось! Вы ничего не получили.'
                users_[str(callback.from_user.id)]['frog']['frog_on_work'] = False
                await bot.send_message(message.chat.id,
                                 text,
                                 message_thread_id=message.message_thread_id)
        
            else:
                await bot.send_message(message.chat.id,
                                       'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!',
                                       message_thread_id=message.message_thread_id)
    
        else:   
            await bot.send_message(message.chat.id,
                                   'Ваша лягушка не может работать пока голодна 🦴!',
                                   message_thread_id=message.message_thread_id)
    
    else:
        await bot.send_message(message.chat.id,
                               'Ваша лягушка уже на работе!',
                               message_thread_id=message.message_thread_id)

    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text = 'fb_w_thief')
async def robber(callback: types.CallbackQuery):
    async def work(message: types.Message, bot: Bot, users_: dict, config: dict):
        if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
            users_[str(callback.from_user.id)]['frog']['has_been_thief'] = True
            print(f'Пользователь {callback.from_user.id} отправил лягушку на работу грабителем')
            await bot.send_message(message.chat.id,
                             '''🔑 Вы успешно отправили вашу лягушку на работу грабителем! Вы сошли с ума?! Она же может попасть в тюрьму!

🕔 Сообщение о результате ограбления придёт через 3 минуты.''',
                                 message_thread_id=message.message_thread_id)
                    
            users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True
            if users_[str(callback.from_user.id)]['frog']['items']['golden_gloves'] == False:
                results = ('successful', 'successful', 'successful', 'cops', 'cops', 'cops', 'cops', 'cops', 'cops', 'cops')
            else:
                results = ('successful', 'successful', 'successful', 'successful', 'successful', 'successful', 'successful', 'cops', 'cops', 'cops')
            result = choice(results)
            await sleep(180)
            users_[str(callback.from_user.id)]['frog']['frog_satiety'] -= 1
            if result == 'successful':
                what_frog_robbed = choice(('аптеку', 'аптеку', 'аптеку', 'музей', 'музей', 'музей', 'дом', 'дом', 'дом', 'дом', 'банк'))
                if what_frog_robbed == 'аптеку': add = randint(225, 290)
                if what_frog_robbed == 'дом': add = randint(150, 375)
                if what_frog_robbed == 'банк': add = randint(375, 500)
                if what_frog_robbed == 'музей': add = randint(475, 550)
                print(f'Лягушка пользователя {callback.from_user.id} успешно ограбила {what_frog_robbed}')

                if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
                    addd = add * config['items_i']['lucky_coin'][str(users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                    addd -= add
                    addd = round(addd)
                    users_[str(callback.from_user.id)]['user']['money'] += addd
                if users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['player_has'] == True:
                    addd = add * config['items_i']['magic_diamond'][str(users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['level'])]
                    addd -= add
                    addd = round(addd)
                    users_[str(callback.from_user.id)]['user']['money'] += addd
                if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
                    add_r = add * int(round(config['rank_multiplier'][str(users_[str(callback.from_user.id)]['frog']['rank'])]))
                    users_[str(callback.from_user.id)]['user']['money'] += add_r
                users_[str(callback.from_user.id)]['user']['money'] += add
                text = f'''Ваша лягушка успешно ограбила {what_frog_robbed}.
Вы получили:
 - 💵 {add} коинов'''
                if addd != 0:
                    text += f'\n - 💵 {addd} коинов (Предметы)'
                if add_r != 0:
                    text += f'\n - 💵 {add_r} коинов (Ранг)'

                elif result == 'cops':
                    users_[str(callback.from_user.id)]['frog']['frog_in_jail'] = True
                    users_[str(callback.from_user.id)]['frog']['has_been_in_jail'] = True
                    users_[str(callback.from_user.id)]['frog']['can_be_cop_after_thief'] = False
                    print(f'Лягушка пользователя {callback.from_user.id} попалась полиции')
                    text = 'О нет! Ваша лягушка попалась полиции и её посадили в тюрьму! 😱'
                users_[str(callback.from_user.id)]['frog']['frog_on_work'] = False
                await bot.send_message(message.chat.id, 
                                 text,
                                 message_thread_id=message.message_thread_id)
        else:
            await bot.send_message(message.chat.id, 
                             'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!',
                             message_thread_id=message.message_thread_id)
        
    await work_template(bot, callback, work, users_, 0, config)

@dp.callback_query_handler(text = 'fb_w_cleaner')
async def cleaner(callback: types.CallbackQuery):
    async def work(message: types.Message, bot: Bot, users_: dict, config: dict):
        print(f'Пользователь {callback.from_user.id} отправил лягушку на работу уборщиком')
        await bot.send_message(message.chat.id, '''Вы успешно отправили вашу лягушку на работу уборщиком 🧹!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.''',
                                     message_thread_id=message.message_thread_id)
        users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True
        await sleep(180)
        users_[str(callback.from_user.id)]['frog']['frog_satiety'] -= 1
        add = randint(50, 75)
        addd = 0
        add_r = 0
        if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
            addd = add * config['items_i']['lucky_coin'][str(users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['level'])]
            addd -= add
            addd = round(addd)
            users_[str(callback.from_user.id)]['user']['money'] += addd
        if users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['player_has'] == True:
            addd = add * config['items_i']['magic_diamond'][str(users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['level'])]
            addd -= add
            addd = round(addd)
            users_[str(callback.from_user.id)]['user']['money'] += addd
        if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
            add_r = add * int(round(config['rank_multiplier'][str(users_[str(callback.from_user.id)]['frog']['rank'])]))
            users_[str(callback.from_user.id)]['user']['money'] += add_r
        users_[str(callback.from_user.id)]['user']['money'] += add
        text = f'''Ваша лягушка провела рабочий день уборщиком, ей заплатили копейки.
Вы получили:
 - 💵 {add} коинов'''
        if addd != 0 or add_r != 0:
            text += '\nБонусы:'

        if addd != 0:
            text += f'\n - 💵 {addd} коинов (Предметы)'
        if add_r != 0:
            text += f'\n - 💵 {add_r} коинов (Ранг)'
        
        users_[str(callback.from_user.id)]['frog']['frog_on_work'] = False

        print(f'Лягушка пользователя {callback.from_user.id} успешно провела рабочий день уборщиком')
        await bot.send_message(message.chat.id,
                               text,
                               message_thread_id=message.message_thread_id)
    
    await work_template(bot, callback, work, users_, 0, config)
    
    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text = 'fb_w_cook')
async def cook(callback: types.CallbackQuery):
    message = callback.message
    async def work(message: types.Message, bot: Bot, users_: dict, config: dict):
        if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
            print(f'Пользователь {message.from_user.id} отправил лягушку на работу поваром')
            await bot.send_message(message.chat.id, '''Вы успешно отправили вашу лягушку на работу поваром 👨‍🍳!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.''',
                                           message_thread_id=message.message_thread_id)
                    
            users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True

            await sleep(180)

            results = (
                'успешно',
                'успешно',
                'успешно',
                'обожглась',
                'обожглась',
                'недожарилась',
                'подгорела',
                'сгорела',
                'сгорела',
                'просрочка'
            )

            result = choice(results)

            users_[str(callback.from_user.id)]['frog']['frog_satiety'] -= 1

            if result == 'успешно':
                print(f'Лягушка пользователя {message.from_user.id} успешно приготовила блюдо')
                add = randint(100, 275)
                if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
                    addd = add * config['items_i']['lucky_coin'][str(users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                    addd -= add
                    addd = round(addd)
                    users_[str(callback.from_user.id)]['user']['money'] += addd
                    print(addd)
                if users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['player_has'] == True:
                    addd = add * config['items_i']['magic_diamond'][str(users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['level'])]
                    addd -= add
                    addd = round(addd)
                    users_[str(callback.from_user.id)]['user']['money'] += addd
                    print(addd)

                if users_[str(callback.from_user.id)]['frog']['rank'] not in [1, 2]:
                    rm = int(round(config['rank_multiplier'][str(users_[str(callback.from_user.id)]['frog']['rank']-1)]))
                    print(rm)
                    add_r = add * rm
                    users_[str(callback.from_user.id)]['user']['money'] += add_r
                users_[str(callback.from_user.id)]['user']['money'] += add
                text = f'''Ваша лягушка успешно приготовила блюдо.
Вы получили:
 - 💵 {add} коинов'''
                if addd != 0:
                    text += f'\n - 💵 {addd} коинов (Предметы)'
                if add_r != 0:
                    text += f'\n - 💵 {add_r} коинов (Ранг)'
                
            elif result == 'недожарилась':
                client = choice(['заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'не заметил', 'не заметил', 'не заметил', 'не заметил'])
                if client == 'заметил':
                    print(f'Лягушка пользователя {message.from_user.id} недожарила блюдо и её уволили')
                    text = 'Ваша лягушка недожарила блюдо, клиент это заметил и её уволили.'
                elif client == 'не заметил':
                    print(f'Лягушка пользователя {message.from_user.id} успешно приготовила блюдо недожаренным, но клиент этого не заметил.')
                    add = randint(50, 175)
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
                        addd = add * config['items_i']['lucky_coin'][str(users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                        addd -= add
                        addd = round(addd)
                        users_[str(callback.from_user.id)]['user']['money'] += addd
                    if users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['player_has'] == True:
                        addd = add * config['items_i']['magic_diamond'][str(users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['level'])]
                        addd -= add
                        addd = round(addd)
                        users_[str(callback.from_user.id)]['user']['money'] += addd

                    if users_[str(callback.from_user.id)]['frog']['rank'] not in [1, 2]:
                        rm = int(round(config['rank_multiplier'][str(users_[str(callback.from_user.id)]['frog']['rank']-1)]))
                        print(rm)
                        add_r = add * rm
                        users_[str(callback.from_user.id)]['user']['money'] += add_r
                    users_[str(callback.from_user.id)]['user']['money'] += add
                    text = f'''Ваша лягушка недожарила блюдо, клиент этого не заметил, но вам заплатили меньше.
Вы получили:
 - 💵 {add} коинов'''
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True or users_[str(callback.from_user.id)]['frog']['rank'] != 1 and users_[str(callback.from_user.id)]['frog']['items']['magic_coin']['player_has']:
                        text += '\nБонусы:'

                    for item in config['items_l']:
                        if users_[str(callback.from_user.id)]['frog']['items'][item]['player_has'] == True:
                            is_add = True
                            break
                    if is_add == True:
                        item_name = config['items_m'][item]
                    text += f'\n - 💵 {addd} коинов {item_name}'
                    if users_[str(callback.from_user.id)]['frog']['rank'] in [1, 2]:
                        text += f'\n - 💵 {add_r} коинов (Ранг)'
                
            elif result == 'подгорела':
                client = choice(['заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'заметил', 'не заметил', 'не заметил'])
                if client == 'заметил':
                    print(f'Лягушка пользователя {message.from_user.id} пережарила блюдо, её уволили.')
                    text = 'Блюдо вашей лягушки подгорело, клиент это заметил и её уволили'
                elif result == 'не заметил':
                    print(f'Лягушка пользователя {message.from_user.id} приготовила блюдо пережаренным, клиент этого не заметил.')
                    add = randint(25, 100)
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
                        addd = add * config['items_i']['lucky_coin'][str(users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['level'])]
                        addd -= add
                        addd = round(addd)
                        users_[str(callback.from_user.id)]['user']['money'] += addd
                    if users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['player_has'] == True:
                        addd = add * config['items_i']['magic_diamond'][str(users_[str(callback.from_user.id)]['frog']['items']['magic_diamond']['level'])]
                        addd -= add
                        addd = round(addd)
                        users_[str(callback.from_user.id)]['user']['money'] += addd

                    if users_[str(callback.from_user.id)]['frog']['rank'] not in [1, 2]:
                        rm = int(round(config['rank_multiplier'][str(users_[str(callback.from_user.id)]['frog']['rank']-1)]))
                        print(rm)
                        add_r = add * rm
                        users_[str(callback.from_user.id)]['user']['money'] += add_r
                    users_[str(callback.from_user.id)]['user']['money'] += add
                    text = f'''У вашей лягушки подгорело блюдо, клиент этого не заметил, но вам заплатили меньше.
Вы получили:
 - 💵 {add} коинов'''
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True or users_[str(callback.from_user.id)]['frog']['rank'] != 1 and users_[str(callback.from_user.id)]['frog']['items']['magic_coin']['player_has']:
                        text += '\nБонусы:'
    
                    for item in config['items_l']:
                        if users_[str(callback.from_user.id)]['frog']['items'][item]['player_has'] == True:
                            is_add = True
                            break
                    if is_add == True:
                        item_name = config['items_m'][item]
                    text += f'\n - 💵 {addd} коинов {item_name}'
                    if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
                        text += f'\n - 💵 {add_r} коинов (Ранг)'
                
            elif result == 'сгорела':
                print(f'Лягушка пользователя {message.from_user.id} сожгла блюдо, её уволили')
                text = 'Блюдо вашей лягушки сгорело, её уволили'
                
            elif result == 'просрочка':
                print(f'Лягушка пользователя {message.from_user.id} успешно приготовила блюдо из просрочки, её уволили')
                text = 'Ваша лягушка приготовила блюдо из просрочки, её уволили'
                    
            elif result == 'обожглась':
                print(f'Лягушка пользователя {message.from_user.id} обожглась')
                users_[str(callback.from_user.id)]['frog']['is_alive'] = False
                text = '''Ваша лягушка получила ожог во время готовки! Какой ужас!
Вы получили:
 - 🔥 Ожог у лягушки (Нужна аптечка)'''

            users_[str(callback.from_user.id)]['frog']['frog_on_work'] = False

            await bot.send_message(message.chat.id,
                                     text,
                                     message_thread_id=message.message_thread_id)
        else:
            await bot.send_message(message.chat.id, 
                             'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!',
                             message_thread_id=message.message_thread_id)
    
    await work_template(bot, callback, work, users_, 0, config)
    
    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text = 'fb_w_killer')
async def killer(callback = types.CallbackQuery):
    message = callback.message
    if users_[str(callback.from_user.id)]['frog']['rank'] >= 4:
        if users_[str(callback.from_user.id)]['frog']['frog_on_work'] == False:
            if users_[str(callback.from_user.id)]['frog']['frog_satiety'] >= 1:
                if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
                    print(f'Пользователь {message.from_user.id} отправил лягушку на работу убийцей')
                    await bot.send_message(message.chat.id,
                                     '''Вы успешно отправили вашу лягушку на работу киллером 🔪!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.
ℹ Предметы дающие дополнительный доход не работают на данной работе''',
                                     message_thread_id=message.message_thread_id)
                    
                    users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True

                    await sleep(180)

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

                    users_[str(callback.from_user.id)]['frog']['frog_satiety'] -= 1

                    if result == 'провал':
                        print(f'Лягушка пользователя {message.from_user.id} попала в тюрьму')
                        users_[str(callback.from_user.id)]['frog']['frog_in_jail'] = True
                        users_[str(callback.from_user.id)]['frog']['has_been_in_jail'] = True
                        users_[str(callback.from_user.id)]['frog']['can_be_cop_after_thief'] = False
                        text = 'О нет! Ваша лягушка попалась полиции и её посадили в тюрьму! 😱'
                    if result == 'успешно':
                        print(f'Лягушка пользователя {message.from_user.id} успешно выполнила заказ...')
                        add = randint(900, 1100)
                        users_[str(callback.from_user.id)]['user']['money'] += add
                        text = f'''Ваша лягушка успешно убила другую лягушку.
Вы получили:
 - 💵 {add} коинов'''

                    users_[str(callback.from_user.id)]['frog']['frog_on_work'] = False

                    await bot.send_message(message.chat.id, 
                                           text,
                                           message_thread_id=message.message_thread_id)

            else:
                await bot.send_message(message.chat.id, 
                                 'Ваша лягушка должна быть на свободе, а не в тюрьме 🔒!',
                                 message_thread_id=message.message_thread_id)
        
        else:
            await bot.send_message(message.chat.id, 
                             'Ваша лягушка не может работать пока голодна 🦴!',
                             message_thread_id=message.message_thread_id)
            
    else:
        await bot.send_message(message.chat.id,
                               'Для отправки лягушку на работу поваром нужен минимум каменный (2) ранг!',
                               message_thread_id=message.message_thread_id)

@dp.callback_query_handler(text = 'fb_u_rank')
async def upgrade_rank(callback: types.CallbackQuery):
    message = callback.message
    if users_[str(callback.from_user.id)]['frog']['rank'] < 8:
        cost = {
            '2': 5000,
            '3': 7500,
            '4': 10000,
            '5': 12500,
            '6': 15000,
            '7': 17500,
            '8': 20000
        }
        brank = users_[str(callback.from_user.id)]['frog']['rank'] + 1
        befrank = users_[str(callback.from_user.id)]['frog']['rank']
        if users_[str(callback.from_user.id)]['user']['money'] >= cost[str(brank)]:
            users_[str(callback.from_user.id)]['user']['money'] -= cost[str(brank)]
            users_[str(callback.from_user.id)]['frog']['rank'] += 1
            rankn = users_[str(callback.from_user.id)]['frog']['rank']
            await bot.send_message(message.chat.id,
                                   f'Вы успешно повысили свой ранг! Ваш прошлый ранг: {config["ranks_values"][str(befrank)]}, ваш текущий ранг: {config["ranks_values"][str(rankn)]}',
                                   message_thread_id=message.message_thread_id)
        else:
            await bot.send_message(message.chat.id,
                                   f'У вас недостаточно монет! Необходимая сумма: {cost[brank]}.',
                                   message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id,
                               'У вас максимальный бесплатный ранг\! ||Да, максимальный __бесплатный__ ранг, у нас скоро будет донат 😉||',
                               parse_mode=types.ParseMode.MARKDOWN_V2,
                               message_thread_id=message.message_thread_id)

@dp.callback_query_handler(text='fb_b_case')
async def buy_case(callback: types.CallbackQuery):
    message = callback.message
    if users_[str(callback.from_user.id)]['user']['event_items']['has_event_items'] == True:
        if users_[str(callback.from_user.id)]['user']['event_items']['candy_2023'] >= 10:
            users_[str(callback.from_user.id)]['user']['cases'] += 1
            users_[str(callback.from_user.id)]['user']['event_items']['candy_2023'] -= 10 
            await bot.send_message(message.chat.id, 'Вы успешно купили кейс!', message_thread_id=message.message_thread_id)
        else:
            await bot.send_message(message.chat.id, 'У вас недостаточно ивентной валюты!', message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id, 'У вас нету ивентной валюты', message_thread_id=message.message_thread_id)

    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text='fb_b_food')
async def buy_food(callback: types.CallbackQuery):
    markup = KeyboardMarkup(row_width=1)

    spider = Button(text='🕷 Паук', callback_data='fb_b_f_spider')
    bug = Button(text='🪲 Жук', callback_data='fb_b_f_bug')
    ant = Button(text='🐜 Муравей', callback_data='fb_b_f_ant')

    markup.add(spider, bug, ant)

    await bot.send_message(callback.message.chat.id, 'Итак, вы решили купить еду лягушке, но какую? 🐜', reply_markup=markup, message_thread_id=callback.message.message_thread_id)

@dp.callback_query_handler(text='fb_b_f_ant')
async def buy_ant(callback: types.CallbackQuery):
    await buy_item_template(callback, users_, 'ant', 50, bot)
    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text='fb_b_f_spider')
async def buy_spider(callback: types.CallbackQuery):
    await buy_item_template(callback, users_, 'spider', 150, bot)
    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text='fb_b_f_bug')
async def buy_ant(callback: types.CallbackQuery):
    await buy_item_template(callback, users_, 'bug', 100, bot)
    save_to_json('users/users.json', users_)

@dp.callback_query_handler(text='fb_b_first_aid_kit')
async def buy_fak(callback: types.CallbackQuery):
    await buy_item_template(callback, users_, 'fak', 100, bot)
    save_to_json('users/users.json', users_)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)