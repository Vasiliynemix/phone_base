# сообщение на команду /start
START_COMMAND_MSG: str = "Добро пожаловать в бота"

# сообщение на кнопку отмена
CANCEL_MSG: str = "Отменено"

# сообщение на кнопку 📱Базы номеров
BASES_MSG: str = "📱Базы номеров"

# Сообщение на инлайн кнопку назад
BACK_MSG: str = "Список баз"

# Сообщение на добавление и изменение csv файла
ADD_CSV_MSG: str = "Загрузите csv файл с базой номеров"

# Не csv файл
ADD_NO_CSV_MSG: str = "Это не csv файл"

# Неверный формат csv файла
ADD_WRONG_FORMAT_CSV_MSG: str = (
    "CSV файл не в нужном формате\n"
    "В нем не может быть ничего кроме номеров в одной колонке\n"
    "Номера в формате 7хххххххххх"
)

# сообщение на успешное изменение файла
EDIT_FILE_SUCCESS_MSG: str = "Файл обновлен"


# Сообщение на добавление названия базы
def phone_name_add_text_msg(added_names: str) -> str:
    return f"Введите название базы, оно должно быть уникальным{added_names}"


# База с названием существует
ADD_PHONE_NAME_EXISTS_MSG: str = "База с таким названием уже существует"


def phone_name_long_msg(name: str) -> str:
    return f"Название слишком длинное, символов должно быть не больше 20. Текущая длина {len(name)}"


# Сообщение добавления текста
ADD_PHONE_TEXT_MSG: str = (
    "Введите текст. Формат:\n{Добрый день|Здравствуйте}!"
    " Вам пишет компания Системы Безопасности\n\n"
    "Мы занимаемся {продажей|реализацией} и {установкой|монтажом}"
    " видеонаблюдения и систем безопасности для коммерческой и частной недвижимости.\n\n"
    "Подскажите, интересно ли вам усилить безопасность вашего дома или бизнеса?\n\n"
    "Слова в шаблоне {...|...|...} будут выбираться рандомно для каждой ссылки."
)


# def phone_text_not
