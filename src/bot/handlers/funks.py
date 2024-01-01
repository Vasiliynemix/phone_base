import csv
import html
import os
import random
import re

import pyperclip
import aiofiles
from aiogram import Bot
from loguru import logger

from src.bot.lexicon.lexicon import COPY_TEXT_ERROR_MSG
from src.config.config import cfg
from src.db.models import Phone


def get_list_random_text(text: str) -> list:
    return re.findall(cfg.regex.random_text_regex, text)


async def get_file_text(bot: Bot, file_id: str) -> str:
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_content = await bot.download_file(file_path)
    text = file_content.read().decode("utf-8")
    cleaned_text = text.replace("\ufeff", "").strip().replace("\r", "")
    return cleaned_text.replace("\n", "|")


def check_file_text(text: str) -> bool:
    text_list = text.split("|")
    for phone in text_list:
        pattern = re.compile(r"^7\d{10}$")
        if not pattern.match(phone):
            return False
    return True


async def create_file_text(text: str, name: str, user_id: int) -> tuple[str, str]:
    numbers = text.split("|")
    root_path = cfg.paths.root_path
    csv_filename = f"{name}.csv"

    path_to_dir_user = os.path.join(root_path, str(user_id))

    path_to_file = os.path.join(path_to_dir_user, csv_filename)
    if not os.path.exists(path_to_dir_user):
        os.makedirs(path_to_dir_user, exist_ok=True)

    async with aiofiles.open(path_to_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        for number in numbers:
            await csv_writer.writerow([number])

    return path_to_dir_user, path_to_file


async def create_text_links(phones: Phone, quantity: int, last_quantity: int) -> str:
    url = "https://wa.me/"

    numbers = phones.numbers.split("|")
    numbers = numbers[last_quantity:]

    text = ""
    for i, number in enumerate(numbers[:quantity]):
        random_text = generate_random_text(phones.text)
        text += f'<a href="{url}{number}?text={random_text}">{i + 1 + last_quantity}. {number}</a>\n'

    return text


def generate_random_text(text: str) -> str:
    matches = get_list_random_text(text)
    for match in matches:
        match_replace = match.replace("{", "").replace("}", "")
        text_list = match_replace.split("|")
        random_element = random.choice(text_list)
        text = text.replace(match, random_element)
        text = (
            text
            .replace("»", "")
            .replace("«", "")
            .replace("%", "")
        )

        text = html.escape(text)

    return text


def split_text(text):
    chunks = []
    while len(text) > 4096:
        last_tag_end = text.rfind("</a>", 0, 4096)
        if last_tag_end == -1:
            break
        chunks.append(text[: last_tag_end + len("</a>")])
        text = text[last_tag_end + len("</a>") :].lstrip()
    if text:
        chunks.append(text)
    return chunks


def copy_text_to_clipboard(text: str, bot: Bot) -> bool:
    try:
        # pattern = r"(\d+\.\s*\d+)\s*\n([\s\S]*?)(?=\d+\.\s*\d+|$)"
        #
        # def replace_block(match):
        #     url = "https://wa.me/"
        #     number_info = match.group(1).split(".")
        #     count = number_info[0]
        #     number = number_info[1]
        #     new_content = f"[{count}\. {number}]({url}{number})\n`{match.group(2)}`\n\n"
        #     return new_content
        #
        # modified_text = re.sub(pattern, replace_block, text)
        # print(modified_text)

        pyperclip.copy(text)
        return True
    except Exception as e:
        logger.error(f"Ошибка копирования в буфер обмена: {e}")
        bot.send_message(chat_id=5254091301, text=COPY_TEXT_ERROR_MSG + str(e))
        return False
