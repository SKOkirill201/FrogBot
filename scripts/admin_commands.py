from aiogram import Bot, types
from users.save import save_to_json

async def admin(bot: Bot, message: types.Message, users_: dict, config: dict):
    if str(message.text).lower().split()[0] in ['/set_value_food', '/set_value_user', '/set_value_frog', '/set_value_items', '/version_info']:
        if len(str(message.text).lower().split()) == 3:
            if message.from_user.id in config['admins']:
                reply = message.reply_to_message
                idd = reply.from_user.id
                print(idd)
                key = str(message.text).lower().split()[1]
                value = str(message.text).lower().split()[2]
                if key in ['rank', 'frog_satiety', 'frog_happines_level']:
                    value = int(value)
                elif key in ['is_alive', 'frog_on_work', 'frog_in_jail', 'has_been_thief',
                             'has_been_in_jail', 'can_be_cop_after_thief']:
                    value = bool(value)
                if str(message.text).lower().split()[0] == '/set_value_frog':
                    if key in ['rank']:
                        value = int(value)
                    users_[str(idd)]['frog'][str(message.text).lower().split()[1]] = value
                elif str(message.text).lower().split()[0] == '/set_value_food':
                    value = int(value)
                    users_[str(idd)]['user']['food'][key] = value
                else:
                    if key in ['money', 'first_aid_kits']:
                        value = int(value)
                    users_[str(idd)]['user'][key] = value
                print(f'Данные пользователя {message.from_user.id} успешно изменены')
                await bot.send_message(message.chat.id,
                                       'Изменения сохранены')
    
        elif len(str(message.text).lower().split()) == 4:
            if message.from_user.id in config['admins']:
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
        
        elif message.text.lower() == '/version_info':
            if message.from_user.id in config['admins']:
                await bot.send_message(message.chat.id,
                                       f'''Информация о версии frog2bot'а:
Версия: {config['bot_info']['version']}
Название коммита: {config['bot_info']['commit_name']}
Релизная версия? {config['bot_info']['release']}
Версия протестирована? {config['bot_info']['tested']}
''',
                                       message_thread_id=message.message_thread_id)
        
        save_to_json('users/users.json', users_)