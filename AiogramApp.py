# Aiogram import | Импортирование Aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup as KMarkup, InlineKeyboardButton as Button

# Time & Random module import | Импортирование модулей Random и Time
from time import sleep as pause
from random import choice, randint
from asyncio import sleep

# Json import | Импорт модуля Json
import json

# Custom scripts imports | Импорты кастомных скриптов
from users.save import save_to_json
from scripts.fb_ff import *
from scripts.change_name import *
from scripts.frog_info import *
from scripts.not_frog_commands import *
from scripts.main_commands import *
from scripts.work_commands import *
from scripts.admin_commands import *

with open('config.json', encoding='utf-8') as alll:
    config = json.load(alll)
    
    token = config['token']

with open('users/users.json', encoding='utf-8') as users: users_ = json.load(users)
with open('other/chats.json', encoding='utf-8') as f: chats = json.load(f)

bot = Bot(token=token)
dp = Dispatcher(bot)

# Команды
@dp.message_handler()
async def messages(message: types.Message):
    await not_frog(bot, message, users_)
    await main(bot, message, users_)
    await work(bot, message, users_, config)
    await frog_info_commands(bot, message, users_, config)
    await admin(bot, message, users_)

    save_to_json('users/users', users_)
    save_to_json('other/chats', chats)

# Feeding frog | Кормим лягушку
# Ant | Муравей
@dp.callback_query_handler(text = 'fb_ff_ant')
async def ff_ant(callback: types.CallbackQuery):
    await fb_ff(callback, bot, users_, 1, 'ants')
    print(f'Пользователь {callback.from_user.id} покормил лягушку муравьём')
# Spider | Паук
@dp.callback_query_handler(text = 'fb_ff_spider')
async def ff_spider(callback: types.CallbackQuery):
    await fb_ff(callback, bot, users_, 3, 'spiders')
    print(f'Пользователь {callback.from_user.id} покормил лягушку пауком')
# Bug | Жук
@dp.callback_query_handler(text = 'fb_ff_bug')
async def ff_bug(callback: types.CallbackQuery):
    await fb_ff(callback, bot, users_, 2, 'bugs')
    print(f'Пользователь {callback.from_user.id} покормил лягушку жуком')

# Negotiate with the police | Договор с полицией
# 300 coins
@dp.callback_query_handler(text = 'fb_nwtp_300c')
async def ff_bug(callback: types.CallbackQuery):
    await negotiate(bot, callback.message, users_, 300, callback)
    print(f'Пользователь {callback.from_user.id} попытался договориться с полицией за 300 коинов')
# 500 coins
@dp.callback_query_handler(text = 'fb_nwtp_500c')
async def ff_bug(callback: types.CallbackQuery):
    await negotiate(bot, callback.message, users_, 500, callback)
    print(f'Пользователь {callback.from_user.id} попытался договориться с полицией за 500 коинов')
# 750 coins
@dp.callback_query_handler(text = 'fb_nwtp_750c')
async def ff_bug(callback: types.CallbackQuery):
    await negotiate(bot, callback.message, users_, 750, callback)
    print(f'Пользователь {callback.from_user.id} попытался договориться с полицией за 750 коинов')

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
                    for item in config['items_l']:
                        if users_[str(callback.from_user.id)]['frog']['items'][item]['player_has'] == True:
                            item_name = config['items_m'][item]
                            text += f'\n - 💵 {addd} коинов {item_name}'
                    if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
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

    save_to_json('users/users', users_)

@dp.callback_query_handler(text = 'fb_w_thief')
async def robber(callback: types.CallbackQuery):
    message = callback.message
    if users_[str(callback.from_user.id)]['frog']['frog_on_work'] == False:
        if users_[str(callback.from_user.id)]['frog']['frog_satiety'] >= 1:
            if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
                users_[str(callback.from_user.id)]['frog']['has_been_thief'] = True
                print(f'Пользователь {callback.from_user.id} отправил лягушку на работу грабителем')
                await bot.send_message(message.chat.id,
                                 '''🔑 Вы успешно отправили вашу лягушку на работу грабителем! Вы сошли с ума?! Она же может попасть в тюрьму!

🕔 Сообщение о результате ограбления придёт через 3 минуты.''',
                                 message_thread_id=message.message_thread_id)
                    
                users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True
                results = ('successful', 'successful', 'successful', 'cops', 'cops', 'cops', 'cops', 'cops', 'cops', 'cops')
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

                    '''if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True or users_[str(callback.from_user.id)]['frog']['rank'] != 1:
                        text += '\nБонусы:'
                    if users_[str(callback.from_user.id)]['frog']['items']['lucky_coin']['player_has'] == True:
                        text += f'\n - 💵 {add_lc} коинов (Коин удачи)'''
                    for item in config['items_l']:
                        if users_[str(callback.from_user.id)]['frog']['items'][item]['player_has'] == True:
                            item_name = config['items_m'][item]
                            text += f'\n - 💵 {addd} коинов {item_name}'
                    if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
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
        else:
            await bot.send_message(message.chat.id, 
                             'Ваша лягушка не может работать пока голодна 🦴!',
                             message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id, 
                         'Ваша лягушка уже на работе!',
                         message_thread_id=message.message_thread_id)

@dp.callback_query_handler(text = 'fb_w_cleaner')
async def cleaner(callback: types.CallbackQuery):
    message = callback.message
    if users_[str(callback.from_user.id)]['frog']['frog_on_work'] == False:
        if users_[str(callback.from_user.id)]['frog']['frog_satiety'] >= 1:
            if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
                print(f'Пользователь {callback.from_user.id} отправил лягушку на работу уборщиком')
                bot.reply_to(message, '''Вы успешно отправили вашу лягушку на работу уборщиком 🧹!

🕔 Сообщение о результате рабочего дня придёт через 3 минуты.''',
                             message_thread_id=message.message_thread_id)
                    
                users_[str(callback.from_user.id)]['frog']['frog_on_work'] = True
                await sleep(180)
                users_[str(callback.from_user.id)]['frog']['frog_satiety'] -= 1
                
                add = randint(50, 75)
                
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
                
                for item in config['items_l']:
                    if users_[str(callback.from_user.id)]['frog']['items'][item]['player_has'] == True:
                        item_name = config['items_m'][item]
                        text += f'\n - 💵 {addd} коинов {item_name}'
                    if users_[str(callback.from_user.id)]['frog']['rank'] != 1:
                        text += f'\n - 💵 {add_r} коинов (Ранг)'
                    
                print(f'Лягушка пользователя {callback.from_user.id} успешно провела рабочий день уборщиком')

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
    
    save_to_json('users/users', users_)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)