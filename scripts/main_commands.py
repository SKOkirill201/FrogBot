from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup as KMarkup, InlineKeyboardButton as Button
from other.commands import all_commands
from users.save import *

async def main(bot: Bot, message: types.Message, users_: dict):
    if str(message.text).lower() in all_commands['get_frog']:
        def frog_check(all_users, id):
            if not id in all_users:
                return False
            else:
                return True
        has_frog = frog_check(users_, str(message.from_user.id))

        if has_frog == False:
            await bot.send_message(message.chat.id, 'Хей! Вы не зарегистрированы в системе! Если хотите зарегистрироватся напишите "старт"', message_thread_id=message.message_thread_id)
        else:
            if users_[str(message.from_user.id)]['have_frog'] == False:
                print(f'Пользователь {message.from_user.id} взял себе лягушку')
                await bot.send_message(message.chat.id, 'Вы отправились в магазин питомцев, долго рассматривали огромную коллекцую из лягушек! Но наконец, выбрали самую лучшую! Теперь вы друзья! Осталось ей только имя дать!', message_thread_id=message.message_thread_id)
                users_[str(message.from_user.id)]['have_frog'] = True

                save_to_json('users/users', users_)
            else:
                await bot.send_message(message.chat.id, 'У вас уже есть лягушка.', message_thread_id=message.message_thread_id)

    # /feed_frog command | Команда /feed_frog
    elif str(message.text).lower() in all_commands['feed_frog']:
        markup = KMarkup(row_width=1)

        ant = Button(text='🐜 Муравьём', callback_data='fb_ff_ant')
        spider = Button(text='🕷 Пауком', callback_data='fb_ff_spider')
        bug = Button(text='🪲 Жуком', callback_data='fb_ff_bug')
        
        markup.insert(ant)
        markup.insert(bug)
        markup.insert(spider)

        await bot.send_message(message.chat.id, 'Вы решили угостить свою лягушку едой, но какой?',
                               reply_markup=markup, 
                               message_thread_id=message.message_thread_id)

    elif str(message.text).lower() in all_commands['use_first_aid_kit']:
        if users_[str(message.from_user.id)]['user']['first_aid_kits'] > 0:
            if users_[str(message.from_user.id)]['frog']['is_alive'] != True:
                users_[str(message.from_user.id)]['user']['first_aid_kits'] -= 1
                users_[str(message.from_user.id)]['frog']['is_alive'] += 20
                bot.send_message(message.chat.id, 
                                 'Вы успешно восстановили здоровье своей лягушке ❤!',
                                 message_thread_id=message.message_thread_id)
            else:
                bot.send_message(message.chat.id, 
                                 'Ваша лягушка в полном порядке ❤',
                                 message_thread_id=message.message_thread_id)
        else:
            bot.send_message(message.chat.id, 
                             'У вас нету аптечек!',
                             message_thread_id=message.message_thread_id)