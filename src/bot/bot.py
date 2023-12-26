from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from loguru import logger

from pkg.logger import Logger
from src.bot.handlers.start import router as start_router
from src.bot.handlers.user.phone_base import router as phone_base_router
from src.bot.middlewares.db import DatabaseMiddleware
from src.bot.middlewares.logger import LoggerMiddleware
from src.bot.structures.transfer_data import TransferData
from src.config.config import cfg
from src.db.db import engine


async def start_bot(log: Logger) -> None:
    bot = Bot(token=cfg.bot.token)
    logger.info(f"START Bot... {await bot.get_my_name()}")

    dp = get_dispatcher()

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(
            engine=engine(url=cfg.db.build_connection_str, level=cfg.logger.level),
            log=log,
        ),  # type: ignore
    )


def get_dispatcher(
    storage: BaseStorage | None = MemoryStorage(),
    fsm_strategy: FSMStrategy | None = FSMStrategy.CHAT,
    event_isolation: BaseEventIsolation | None = None,
) -> Dispatcher:
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation,
    )

    dp.include_router(router=start_router)

    dp.include_router(router=phone_base_router)

    dp.message.outer_middleware(DatabaseMiddleware())
    dp.callback_query.outer_middleware(DatabaseMiddleware())

    dp.message.middleware(LoggerMiddleware())
    dp.callback_query.middleware(LoggerMiddleware())

    return dp
