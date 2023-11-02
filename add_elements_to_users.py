from users.save import save_to_json
import json

with open('users/users.json', encoding='utf-8') as users:
    users_ = json.load(users)

for i in list(users_.keys()):
    users_[i]['user']['event_items'] = {
        "has_event_items": False,
        "candy_2023": 0
    }

save_to_json('users/users.json', users_)