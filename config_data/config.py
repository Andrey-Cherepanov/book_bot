from dataclasses import dataclass
from environs import Env

# Класс с конфигурацией бота
@dataclass
class TgBot:
    token: str

# Класс конфигурации
@dataclass
class Config:
    tg_bot: TgBot

# Функция получения конфигурации
def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(
                               token=env('BOT_TOKEN'))
                  )
