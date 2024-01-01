import re


def replace_text_blocks(original_text):
    pattern = r"(\d+\.\s*\d+)\s*\n([\s\S]*?)(?=\d+\.\s*\d+|$)"

    def replace_block(match):
        url = "https://wa.me/"
        number_info = match.group(1).split(".")
        count = number_info[0].strip()
        number = number_info[1].strip()
        new_content = f"[{count}\. {number}]({url}{number})\n`{match.group(2)}`\n\n"
        return new_content

    modified_text = re.sub(pattern, replace_block, original_text)

    return modified_text


# Пример исходного текста
original_text = """
261. 79955650856
Здравствуйте! Вам пишет компания Системы Безопасности

йцукенг

Мы занимаемся реализацией и установкой видеонаблюдения и систем безопасности для коммерческой и частной недвижимости.

йцукен

Подскажите, интересно ли вам усилить безопасность вашего дома или бизнеса?

262. 79955695225
Добрый день! Вам пишет компания Системы Безопасности

Мы занимаемся продажей и монтажом видеонаблюдения и систем безопасности для коммерческой и частной недвижимости.

Подскажите, интересно ли вам усилить безопасность вашего дома или бизнеса?
"""

# Заменяем текстовые блоки между номерами
modified_text = replace_text_blocks(original_text)

print(modified_text)
