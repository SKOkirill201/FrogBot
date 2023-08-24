import json
import os.path

def save_to_json(dir, add):
    if os.path.exists(dir) == True:
        if os.path.isfile(dir) == True:
            with open(dir, 'w', encoding='utf-8') as file:
                json.dump(add, file, indent=4)
        else:
            raise Exception('Указанный файл не является файлом')
    else:
        raise FileNotFoundError('Данного файла не существует!')

def load_from_json(dir):
    if os.path.exists(dir) == True:
        if os.path.isfile(dir) == True:
            with open(dir, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            raise Exception('Указанный файл не является файлом')
    else:
        raise FileNotFoundError('Данного файла не существует!')