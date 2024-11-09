from dataclasses import dataclass, field
from typing import Literal
from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import URL


load_dotenv()


@dataclass
class BotConfig:
    token: str = os.getenv("BOT_TOKEN")


@dataclass
class DBConfig:
    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USERNAME")
    passwd: str = os.getenv("DB_PASSWORD")
    port: int = int(os.getenv("DB_PORT"))
    host: str = os.getenv("DB_HOST")

    driver: str = os.getenv("DRIVER")
    database_system: str = os.getenv("DATABASE_SYSTEM")

    limit_phones: int = 10

    @property
    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class LogConfigPathName:
    info_log_file_name: str = os.getenv("INFO_LOG_FILE_NAME")
    debug_log_file_name: str = os.getenv("DEBUG_LOG_FILE_NAME")


@dataclass
class LogConfig:
    level: Literal["debug", "info"] = os.getenv("LOG_LEVEL")
    log_dir: str = os.getenv("LOG_DIR_NAME")

    file_name: LogConfigPathName = field(default_factory=LogConfigPathName)


@dataclass
class PathConfig:
    root_path: str = str(Path(__file__).parent.parent.parent)
    log_config: LogConfig = field(default_factory=LogConfig)

    @property
    def log_directory_path(self):
        return os.path.join(self.root_path, self.log_config.log_dir)

    @property
    def info_log_path(self):
        return os.path.join(
            self.root_path,
            self.log_config.log_dir,
            self.log_config.file_name.info_log_file_name,
        )

    @property
    def debug_log_path(self):
        return os.path.join(
            self.root_path,
            self.log_config.log_dir,
            self.log_config.file_name.debug_log_file_name,
        )

    @staticmethod
    def __create_path(path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)


@dataclass
class ReConfig:
    random_text_regex: str = "\{[^{}]*\|[^{}]*\}"  # noqa
    param_text_regex: str = r"\{(param1|param2)\}"  # noqa


@dataclass
class Config:
    time_format: str = os.getenv("TIME_FORMAT")
    logger: LogConfig = field(default_factory=LogConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    bot: BotConfig = field(default_factory=BotConfig)
    db: DBConfig = field(default_factory=DBConfig)
    regex: ReConfig = field(default_factory=ReConfig)


cfg = Config()
