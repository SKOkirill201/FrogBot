from aiogram import Bot, types
from users.save import save_to_json
from random import choice, randint
from other.commands import all_commands
from aiogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as KeyboardMarkup
import json

with open('storage.json', encoding='utf-8') as f:
    storage = json.load(f)

gifts_ = {

}

items_ = {

}

texts = {
    "0": "Обычный",
    "1": "Редкий",
    "2": "Сверхредкий",
    "3": "Легендарный",
    "ancient_coin": "Древний коин",
    "ancient_sword": "Древний меч",
    "lucky_potion": "Зелье удачи"
}

async def open_case(bot: Bot, message: types.Message, users_: dict, config: dict):
    if users_[str(message.from_user.id)]['user']['cases'] > 0:
        prizes = (
            'coin', 'coin', 'coin', 'coin', 'coin',
            'candy', 'candy', 'candy', 'ant', 'ant',
            'ant', 'ant', 'ant', 'first_aid_kit', 'first_aid_kit',
            'ancient_coin', 'lucky_potion', 'ancient_sword'
        )
        prize = choice(prizes)
        if prize in ('ancient_coin', 'lucky_potion', 'ancient_sword'):
            rarities = [
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                1, 1, 1, 1, 1,
                1, 1, 1, 1, 1,
                1, 1, 1, 1, 1,
                1, 1, 1, 1, 1,
                1, 1, 1, 1, 1,
                2, 2, 2, 2, 2,
                2, 2, 2, 2, 2,
                2, 2, 2, 2, 2,
                3, 3, 3, 3, 3,
                3, 3, 3, 3, 3]
            rarity = choice(rarities)
            if users_[str(message.from_user.id)]['user']['rare_items'][prize]['player_have'] == False:
                users_[str(message.from_user.id)]['user']['rare_items'][prize]['player_have'] = True
                users_[str(message.from_user.id)]['user']['rare_items'][prize]['rarity'] = rarity
                users_[str(message.from_user.id)]['user']['rare_items']['have_rare_items'] = True
                await bot.send_message(message.chat.id, f'''Поздравляем! Вы получили {texts[prize]} ({texts[str(rarity)]})!''')
            else:
                if rarity > users_[str(message.from_user.id)]['user']['rare_items'][prize]['rarity']:
                    markup = KeyboardMarkup(row_width=2)
                    yes = Button('Да', callback_data='fb_c_ri_yes')
                    no = Button('Нет', callback_data='fb_c_ri_no')
                    markup.add(yes, no)
                    items_[f'{message.chat.id}_{message.from_user.id}'] = {
                        'rarity': rarity,
                        'item': prize
                    }
                    await bot.send_message(message.chat.id, 'Выпал предмет, который у вас уже есть, но его редкость выше чем вашего предмета, заменить предмет?', reply_markup=markup)
                    save_to_json('storage.json', storage)
                else:
                    users_[str(message.from_user.id)]['user']['money'] += 1000
                    await bot.send_message(message.chat.id, 'У вас уже есть данный предмет! Вы получили 1000 коинов!')
        elif prize == 'coin':
            gain = randint(200, 2000)
            users_[str(message.from_user.id)]['user']['money'] += gain
            await bot.send_message(message.chat.id, f'Поздравляем! Вы получили коин! ({gain})')
        elif prize == 'candy':
            gain = randint(1, 10)
            users_[str(message.from_user.id)]['user']['event_items']['candy_2023'] += gain
            await bot.send_message(message.chat.id, f'Поздравляем! Вы получили конфету! ({gain})')
        elif prize == 'ant':
            gain = randint(1, 7)
            users_[str(message.from_user.id)]['user']['food']['ants'] += gain
            await bot.send_message(message.chat.id, f'Поздравляем! Вы получили муравья! ({gain})')
        elif prize == 'first_aid_kit':
            gain = randint(1, 7)
            users_[str(message.from_user.id)]['user']['first_aid_kits'] += gain
            await bot.send_message(message.chat.id, f'Поздравляем! Вы получили аптечку! ({gain})')
        users_[str(message.from_user.id)]['user']['cases'] -= 1
    else:
        await bot.send_message(message.chat.id, 'У вас нету кейсов!')

    save_to_json('users/users.json', users_)
    save_to_json('storage.json', storage)