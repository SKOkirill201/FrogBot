from aiogram import Bot, types

async def buy_item_template(call: types.CallbackQuery, users_: dict, type: str, cost: int, bot: Bot):
    item = {
        "spider": {
            "json": "spiders",
            "user": "паука"
        },
        "ant": {
            "json": "ants",
            "user": "муравья"
        },
        "bug": {
            "json": "bugs",
            "user": "жука"
        },
        "fak": {
            "json": "first_aid_kits",
            "user": "аптечки"
        }
    }
    
    if users_[str(call.from_user.id)]['user']['money'] >= cost:
        users_[str(call.from_user.id)]['user']['money'] -= cost
        if type in ['bug', 'ant', 'spider']:
            users_[str(call.from_user.id)]['user']['food'][item[type]['json']] += 1
        else:
            users_[str(call.from_user.id)]['user'][item[type]['json']] += 1
        await bot.send_message(call.message.chat.id, f'Вы успешно купили {item[type]["user"]} для своей лягушки 🐸!',
                            message_thread_id=call.message.message_thread_id)
    else:
        await bot.send_message(call.message.chat.id, f'''Недостаточно средств для совершения операции покупки {item[type]["user"]}!
Необходимая сумма: {cost} коинов 💸''', message_thread_id=call.message.message_thread_id)