from aiogram import Bot, types
from users.save import save_to_json

async def admin(bot: Bot, message: types.Message, users_: dict):
    print(1)
    if str(message.text).lower().split()[0] in ['/set_value_food', '/set_value_user', '/set_value_frog', '/set_value_items']:
        if len(str(message.text).lower().split()) == 3:
            if message.from_user.id == 2006262756:
                reply = message.reply_to_message
                idd = reply.from_user.id
                print(idd)
                key = str(message.text).lower().split()[1]
                value = str(message.text).lower().split()[2]
                if str(message.text).lower().split()[0] == '/set_value_frog':
                    users_[str(idd)]['frog'][str(message.text).lower().split()[1]] = str(message.text).lower().split()[2]
                elif str(message.text).lower().split()[0] == '/set_value_food':
                    value = int(value)
                    users_[str(idd)]['user']['food'][key] = value
                else:
                    if key == 'money':
                        value = int(value)
                    users_[str(idd)]['user'][key] = value
                print(f'Данные пользователя {message.from_user.id} успешно изменены')
                await bot.send_message(message.chat.id,
                                       'Изменения сохранены')
    
        elif len(str(message.text).lower().split()) == 4:
            if message.from_user.id == 2006262756:
                reply = message.reply_to_message
                idd = reply.from_user.id
                key1 = str(message.text).lower().split()[1]
                key2 = str(message.text).lower().split()[2]
                value = str(message.text).lower().split()[3]
                if str(message.text).lower().split()[0] == '/set_value_items':
                    if key2 == 'level':
                        value = int(value)
                    else:
                        value = bool(value)
                    users_[str(idd)]['frog']['items'][key1][key2] = value
                print(f'Данные пользователя {message.from_user.id} успешно изменены')
                await bot.send_message(message.chat.id,
                                       'Изменения сохранены')
        save_to_json('users/users', users_)