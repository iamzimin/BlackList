import os

from log import Log

BASE_CONFIG = """# Название таблицы
table_name=PUBG

# Минимальная длинна распознавания ников с фото
minimum_nickname_length=2

# Максимальная длинна сравнения ников (-1 для точного сравнения). 
# При значении 6 будут сравниваться только первые 6 символов. Например, "player5" и "player123" будут равны
# Сделано так как длинные ники могут обрезаться и найденный ник с фото "player123456..." не найдётся по базе
maximum_nickname_compare=12

# Автозаполнение полей при вводе ника (если такой есть в чёрном списке). True или False
find_by_name=True

# Автозамена символов при поиске ников с фото по чёрному списку
# Сделано так как OCR иногда ошибается в распознавании схожих символов
# При наличии символов может найти несуществующих игроков ({} чтобы убрать автозамену)
identical_characters={"b":"6", "g":"q", "g":"9", "q":"9", "l":"I", "0":"O", "z":"2", "z":"7"}"""

# Default
TABLE_NAME = "PUBG"
MINIMUM_NICKNAME_LENGTH = 2
MAXIMUM_NICKNAME_COMPARE = 12
FIND_BY_NAME = True
IDENTICAL_CHARACTERS = {"b":"6", "g":"q", "g":"9", "q":"9", "l":"I", "0":"O", "z":"2", "z":"7"}


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read_config(self):
        global TABLE_NAME, MINIMUM_NICKNAME_LENGTH, MAXIMUM_NICKNAME_COMPARE, FIND_BY_NAME, IDENTICAL_CHARACTERS
        if not os.path.exists(self.config_file_path):
            self.save_config()

        try:
            with open(self.config_file_path, 'r') as file:
                config_data = file.read()
            config_lines = config_data.split('\n')

            for line in config_lines:
                try:
                    split = line.split('=')
                    key = split[0].strip()
                    value = split[1].strip()
                except Exception:
                    continue

                try:
                    if key == 'table_name':
                        TABLE_NAME = value if not value == '' else "NoName"
                    elif key == 'minimum_nickname_length':
                        MINIMUM_NICKNAME_LENGTH = max(1, int(value))
                    elif key == 'maximum_nickname_compare':
                        MAXIMUM_NICKNAME_COMPARE = max(-1, int(value))
                    elif key == 'find_by_name':
                        if value.lower() == "false":
                            FIND_BY_NAME = False
                        elif value.lower() == "true":
                            FIND_BY_NAME = True
                        else:
                            raise ValueError
                    elif key == 'identical_characters':
                        IDENTICAL_CHARACTERS = eval(value)
                except Exception:
                    Log.save_log(f"Неверное составление файла конфигурации (поля {key}). "
                                 f"Удалите конфиг файл, чтобы вернуть значения по умолчанию.")
                    raise Exception(f"Неверное составление файла конфигурации (поля {key}). "
                                    f"Удалите конфиг файл, чтобы вернуть значения по умолчанию.")

        except FileNotFoundError:
            self.save_config()
            Log.save_log("Файл конфигурации не найден. Используются значения по умолчанию.")

    def save_config(self):
        with open(self.config_file_path, 'w') as file:
            file.write(BASE_CONFIG)
