import os

from log import Log

BASE_CONFIG = """# Название таблицы
table_name=PUBG

# Минимальная длинна распознавания ников с фото
minimum_nickname_length=2

# Максимальная длинна сравнения ников (-1 для точного сравнения). 
# При значении 6 будут сравниваться только первые 6 символов. Например, "player5" и "player123" будут равны
# Сделано тк длинные ники могут обрезаться и найденный ник с фото "player123456..." не найдётся по базе
maximum_nickname_compare=12

# Автозаполнение полей при вводе ника (если такой есть в чёрном списке). True или False
find_by_name=True"""

# Default
TABLE_NAME = "PUBG"
MINIMUM_NICKNAME_LENGTH = 1
MAXIMUM_NICKNAME_COMPARE = -1
FIND_BY_NAME = True


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read_config(self):
        global TABLE_NAME, MINIMUM_NICKNAME_LENGTH, MAXIMUM_NICKNAME_COMPARE, FIND_BY_NAME
        if not os.path.exists(self.config_file_path):
            self.save_config()

        try:
            with open(self.config_file_path, 'r') as file:
                config_data = file.read()
            config_lines = config_data.split('\n')

            for line in config_lines:
                try:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                except Exception:
                    continue

                try:
                    if key == 'table_name':
                        TABLE_NAME = value
                    elif key == 'minimum_nickname_length':
                        MINIMUM_NICKNAME_LENGTH = max(1, int(value))
                    elif key == 'maximum_nickname_compare':
                        MAXIMUM_NICKNAME_COMPARE = max(0, int(value))
                    elif key == 'find_by_name':
                        FIND_BY_NAME = False if value.lower() == "false" else True
                except ValueError:
                    self.save_config()
                    Log.save_log("Неверное составление файла конфигурации. Используются значения по умолчанию.")
                    exit(1)

        except FileNotFoundError:
            self.save_config()
            Log.save_log("Файл конфигурации не найден. Используются значения по умолчанию.")
            exit(1)

    def save_config(self):
        with open(self.config_file_path, 'w') as file:
            file.write(BASE_CONFIG)
