import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import user_handlers, other_handlers

# init logger
logger = logging.getLogger(__name__)

# bot main func
async def main():
    # config logging
    logging.basicConfig(level=logging.INFO,
                       format='%(filename)s:%(lineno)d #%(levelname)-8s '
                       '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    # load configs
    config = load_config()

    # init bot and dispatcher objects
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

    # set main menu
    await set_main_menu(bot)

    # register routers
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# starting bot
if __name__ == '__main__':
    asyncio.run(main())
