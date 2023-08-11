import json

def save_to_json(dir, add):
    with open(f'{dir}.json', 'w', encoding='utf-8') as file:
        json.dump(add, file, indent=4)