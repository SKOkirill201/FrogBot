from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup as KMarkup, InlineKeyboardButton as Button
from other.commands import all_commands
from random import choice, randint
import json

async def work(bot: Bot, message: types.Message, users_: dict, config: dict):
    if str(message.text).lower() in all_commands['buy_frog_out_of_prison']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            if users_[str(message.from_user.id)]['frog']['frog_in_jail'] == True:
                if users_[str(message.from_user.id)]['user']['money'] >= 325:
                    users_[str(message.from_user.id)]['frog']['frog_in_jail'] = False
                    users_[str(message.from_user.id)]['user']['money'] -= 325
                    await bot.send_message(message.chat.id, 
                                     'Вы успешно выкупили лягушку из тюрьмы 🐸', 
                                     message_thread_id=message.message_thread_id)
                else:
                    await bot.send_message(message.chat.id,
                                     '''У вас недостаточно средств для выкупа лягушки из тюрьмы.
Необходимая сума: 325 коинов 💵''', 
                                     message_thread_id=message.message_thread_id)
            else:
                await bot.send_message(message.chat.id, 
                                 'Ваша лягушка на свободе 🐸',
                                 message_thread_id=message.message_thread_id)
        else:
            await bot.send_message(message.chat.id, 
                             'У вас нету лягушки!',
                             message_thread_id=message.message_thread_id)

    elif str(message.text).lower() in all_commands['negotiate_with_the_police']:
        if users_[str(message.from_user.id)]['has_frog'] == False:
            bot.send_message(message.chat.id,
                             'У вас нету лягушки!',
                             message_thread_id=message.message_thread.id)

        else:
            markup = KMarkup(row_width=3)
    
            coins300 = Button(text='💲 300 Коинов', callback_data='fb_nwtp_300c')
            coins500 = Button(text='💵 500 Коинов', callback_data='fb_nwtp_500c')
            coins750 = Button(text='💰 750 коинов', callback_data='fb_nwtp_750c')
    
            markup.insert(coins300)
            markup.insert(coins500)
            markup.insert(coins750)
    
            await bot.send_message(message.chat.id, 
                         'Вы решили договориться с полицией насчёт работы вашей лягушки грабителем. Сколько вы заплатите им?',
                         reply_markup=markup,
                         message_thread_id=message.message_thread_id)

    elif str(message.text).lower() in all_commands['send_frog_to_work']:
        if users_[str(message.from_user.id)]['have_frog'] == True:
            markup = KMarkup(row_width=1)

            tip = choice(config['tips'])

            office_worker = Button(text='📄 Лягушка будет офисным работником!', callback_data='fb_w_office_worker')
            police = Button(text='👮‍♂️ Лягушка будет полицейским!', callback_data='fb_w_police')
            cleaner = Button(text='🧹 Лягушка будет уборщиком!', callback_data='fb_w_cleaner')
            cook = Button(text='👨‍🍳 Лягушка будет поваром!', callback_data='fb_w_cook')
            programmer = Button(text='👨‍💻 Лягушка будет программистом!', callback_data='fb_w_programmer')
            thief = Button(text='🔓 Лягушка будет вором!', callback_data='fb_w_thief')
            killer = Button(text='🔪 Лягушка будет убийцей!', callback_data='fb_w_killer')
            white_hacker = Button(text='💻 Лягушка будет белым хакером!', callback_data='fb_w_white_hacker')
            hacker = Button(text='👨‍💻 Лягушка будет хакером!', callback_data='fb_w_hacker')
            miner = Button(text='⛏ Лягушка будет шахтёром!', callback_data='fb_w_miner')
            lumberjack = Button(text='🪓 Лягушка будет лесорубом!', callback_data='fb_w_jumberjack')
            farmer = Button(text='👨‍🌾 Лягушка будет фермером!', callback_data='fb_w_farmer')
            builder = Button(text='🏗 Лягушка будет строителем!', callback_data='fb_w_builder')

            markup.insert(office_worker)
            markup.insert(programmer)
            markup.insert(white_hacker)
            markup.insert(hacker)
            markup.insert(thief)
            markup.insert(killer)
            markup.insert(police)
            markup.insert(cook)
            markup.insert(cleaner)
            markup.insert(miner)
            markup.insert(lumberjack)
            markup.insert(farmer)
            markup.insert(builder)

            await bot.send_message(message.chat.id, 
                         f'''Наконец, вы решили отправить свою лягушку на работу! Перед вами выбор, сделать свою лягушку нарушителем закона, или честным офисным работником?

ℹ {tip}''',
                         reply_markup=markup,
                         message_thread_id=message.message_thread_id)

async def negotiate(bot: Bot, message: types.Message, users_: dict, coinsc: int, callback: types.CallbackQuery):
    if users_[str(callback.from_user.id)]['frog']['can_be_cop_after_thief'] == False:
        if users_[str(callback.from_user.id)]['user']['money'] >= coinsc:
            with open('config.json', encoding='utf-8') as f:
                r = json.load(f)
                readed = r['negotiate']

            users_[str(callback.from_user.id)]['user']['money'] -= coinsc
            
            number = randint(0, 100)
            if number <= readed[str(coinsc)]['max']: result = 'fail'
            else: result = 'good'

            if result == 'fail':
                await bot.send_message(message.chat.id,
                                 'Вы не смогли договориться с полицией, вы просто потратили свои коины.',
                                 message_thread_id=message.message_thread_id)
                print(f'Пользователь {callback.from_user.id} не смог договориться с полицией')
            else:
                await bot.send_message(message.chat.id,
                                 'Вы успешно договорились с полицией, теперь ваша лягушка может работать полицейским, хоть и с зарплатой в 2 раза меньше!',
                                 message_thread_id=message.message_thread_id)
                users_[str(callback.from_user.id)]['frog']['can_be_cop_after_thief'] = True
                print(f'Пользователь {callback.from_user.id} договорился с полицией')
        else:
            await bot.send_message(message.chat.id,
                             'У вас недостаточно коинов!',
                             message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id,
                         'Ваша лягушка уже может работать полицейским',
                         message_thread_id=message.message_thread_id)