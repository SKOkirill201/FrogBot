from aiogram import Bot, types
from asyncio import sleep

async def work_template(bot: Bot, callback: types.CallbackQuery, 
                        code, users_: dict, rank: int, config: dict):
    message = callback.message
    values = config['ranks_values']
    rank_ = values[str(rank)]
    if users_[str(callback.from_user.id)]['has_frog'] == True:
        if users_[str(callback.from_user.id)]['frog']['rank'] >= rank:
            if users_[str(callback.from_user.id)]['frog']['frog_on_work'] == False:
                if users_[str(callback.from_user.id)]['frog']['frog_satiety'] >= 1:
                    if users_[str(callback.from_user.id)]['frog']['frog_in_jail'] == False:
                        await code(message, bot, users_, config)
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
        else:
            await bot.send_message(message.chat.id,
                                   f'Для отправки лягушку на данную работу нужен минимум {rank_} ({rank}) ранг!',
                                   message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id,
                               'У вас нету лягушки!',
                               message_thread_id=message.message_thread_id)