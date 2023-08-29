from aiogram import Bot, types
from users.save import *

async def fb_ff(callback: types.CallbackQuery, bot: Bot, users_, satiety, script_name):
    if users_[str(callback.from_user.id)]['has_frog'] == False:
        bot.send_message(callback.message.chat.id,
                         'У вас нету лягушки!',
                         message_thread_id=callback.message.message_thread.id)
    else:
        names = {
            'ants': {
                'emoji': '🐜',
                'success': 'муравьём',
                'out_of': 'муравья'
            },
            'spiders': {
                'emoji': '🕷',
                'success': 'пауком',
                'out_of': 'паука'
            },
            'bugs': {
                'emoji': '🪲',
                'success': 'жуком',
                'out_of': 'жука'
            }
        }
        success = names[script_name]['success']
        emoji = names[script_name]['emoji']
        out_of = names[script_name]['out_of']
        if users_[str(callback.from_user.id)]['frog']['frog_satiety'] < 10:
            if users_[str(callback.from_user.id)]['user']['food'][script_name] > 0:
                users_[str(callback.from_user.id)]['frog']['frog_satiety'] += satiety
                users_[str(callback.from_user.id)]['user']['food'][script_name] -= 1
                await bot.send_message(callback.message.chat.id, f'Вы успешно накормили свою лягушку {success} {emoji}!',
                                       message_thread_id=callback.message.message_thread_id)
            else:
                await bot.send_message(callback.message.chat.id, f'У вас нету ни одного {out_of} {emoji}!',
                                       message_thread_id=callback.message.message_thread_id)

    save_to_json('users/users.json', users_)