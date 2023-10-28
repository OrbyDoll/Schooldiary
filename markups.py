from aiogram import types

menu = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Оценки", callback_data="marks"),
    types.InlineKeyboardButton("Домашка", callback_data="hometask"),
    types.InlineKeyboardButton("Социальная активность", callback_data="socialrate"),
)

admin_menu = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Изменить дз", callback_data="edit_hometask"),
    types.InlineKeyboardButton("Изменить оценки", callback_data="edit_marks"),
    types.InlineKeyboardButton(
        "Побаловаться с соц. рейтингом", callback_data="edit_socialrate"
    ),
)
admin_menu.row(
    types.InlineKeyboardButton(
        "Назад к обычным смертным", callback_data="back_to_start"
    )
)

admin_task = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Добавить дз", callback_data="add_hometask"),
    types.InlineKeyboardButton("Удалить дз", callback_data="del_hometask"),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

file_exist = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Да", callback_data="file_exists"),
    types.InlineKeyboardButton("Нет", callback_data="file_not_exists"),
)

back_to_dates = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад", callback_data="back_to_dates")
)

admin_back_to_dates = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад", callback_data="del_hometask")
)

back_to_menu = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu")
)

hide = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Скрыть", callback_data="hide")
)


def get_dates_markup(date_list):
    date_markup = types.InlineKeyboardMarkup(row_width=3)
    for date in date_list:
        date_markup.insert(
            types.InlineKeyboardButton(date[0], callback_data=f"gettasklist_{date[0]}")
        )
    date_markup.row(
        types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu")
    )
    return date_markup


def get_files_markup(task_list):
    file_markup = types.InlineKeyboardMarkup(row_width=1)
    for task in task_list:
        if task[3][1:] != "None":
            file_markup.insert(
                types.InlineKeyboardButton(
                    f"{task[1]} - Файлы", callback_data=f"file_{task[0]}_{task[1]}"
                )
            )
    file_markup.add(types.InlineKeyboardButton("Назад", callback_data="hometask"))
    return file_markup


def get_del_task_markup(task_list, date):
    task_markup = types.InlineKeyboardMarkup(row_width=2)
    for task in task_list:
        task_markup.insert(
            types.InlineKeyboardButton(
                task[1], callback_data=f"deltask_{date}_{task[1]}"
            )
        )
    task_markup.row(
        types.InlineKeyboardButton(
            "Удалить полностью", callback_data=f"deltask_{date}_all"
        )
    )
    task_markup.row(
        types.InlineKeyboardButton("Назад к датам", callback_data=f"del_hometask")
    )
    return task_markup
