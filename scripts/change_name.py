from aiogram import Bot, types

async def change_name(bot: Bot, message: types.Message, users_, pop_count):
    if users_[str(message.from_user.id)]['have_frog'] == True:
        print('stage 1')
        old_name = users_[str(message.from_user.id)]['frog']['frog_name']

        message_text_split = message.text.split()
        message_text_split.pop(0)
        if pop_count == 3:
            print('stage 2')
            message_text_split.pop(0)
            message_text_split.pop(0)
        name = ' '.join(message_text_split)
            
        if name == old_name:
            print('stage 3')
            await bot.send_message(message.chat.id,
                                   'Старое имя такое же как новое!',
                                   message_thread_id=message.message_thread_id)
        else:
            print('alt stage 3')
            users_[str(message.from_user.id)]['frog']['frog_name'] = name
            await bot.send_message(message.chat.id,
                               f'Вы успешно изменили имя вашей лягушке  🏷! Старое имя: {old_name}, новое имя: {name} 🐸',
                               message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id,
                               'У вас нету лягушки!',
                               message_thread_id=message.message_thread_id)