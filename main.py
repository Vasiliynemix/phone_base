import asyncio

from loguru import logger

from src.bot.bot import start_bot
from src.config.config import cfg
from pkg.logger import Logger


async def main() -> None:
    log = Logger(
        level=cfg.logger.level,
        path_directory="logs",
        info_log_path=cfg.paths.info_log_path,
        debug_log_path=cfg.paths.debug_log_path,
    )
    log.setup_logger()
    logger.debug("Debug mode is on")

    await start_bot(log)


if __name__ == "__main__":
    asyncio.run(main())
