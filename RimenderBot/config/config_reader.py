import configparser
from dataclasses import dataclass


@dataclass
class Bot:
    BOT_TOKEN: str
    ADMIN_ID: int


@dataclass
class Config:
    tg_bot: Bot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    settings = config['BOT_CONFIG']

    return Config(
        tg_bot=Bot(
            BOT_TOKEN=settings['BOT_TOKEN'],
            ADMIN_ID=int(settings['ADMIN_ID'])
        )
    )


if __name__ == '__main__':
    config_ = load_config(r'Z:\Troshkin Artem\Pt9\Maxim Markovtsov\RimenderBot\config\config.ini')
    print(config_.tg_bot.BOT_TOKEN)
    print(config_.tg_bot.ADMIN_ID)
