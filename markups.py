from aiogram import types
import datetime
weekdays = ['Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
menu = types.InlineKeyboardMarkup(row_width=3).add(
    types.InlineKeyboardButton("Оценки", callback_data="marks"),
    types.InlineKeyboardButton("Домашка", callback_data="hometask"),
    types.InlineKeyboardButton('Расписание', callback_data='schedule'),
    types.InlineKeyboardButton("Социальная активность", callback_data="socialrate"),
)

admin_menu = types.InlineKeyboardMarkup(row_width=3).add(
    types.InlineKeyboardButton("Изменить дз", callback_data="edit_hometask"),
    types.InlineKeyboardButton("Изменить оценки", callback_data="edit_marks"),
    types.InlineKeyboardButton("Соц. рейтингом", callback_data="edit_socialrate"),
    types.InlineKeyboardButton('Импорт оценок', callback_data='marks_import')
).row(
    types.InlineKeyboardButton(
        "Назад к обычным смертным", callback_data="back_to_start"
    )
)

marks_choose = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('Добавить оценки', callback_data='marks_add'),
    types.InlineKeyboardButton('Заменить оценки', callback_data='marks_replace'),
)

admin_task = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Добавить дз", callback_data="add_hometask"),
    types.InlineKeyboardButton("Удалить дз", callback_data="del_hometask"),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

schedule = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton('Понедельник', callback_data='dayПонедельник'),
    types.InlineKeyboardButton('Вторник', callback_data='dayВторник'),
    types.InlineKeyboardButton('Среда', callback_data='dayСреда'),
    types.InlineKeyboardButton('Четверг', callback_data='dayЧетверг'),
    types.InlineKeyboardButton('Пятница', callback_data='dayПятница'),
    types.InlineKeyboardButton('Суббота', callback_data='dayСуббота'),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

marks = types.InlineKeyboardMarkup(row_width=3).add(
    types.InlineKeyboardButton('Математика', callback_data='gradeМатематика'),
    types.InlineKeyboardButton('Физика', callback_data='gradeФизика'),
    types.InlineKeyboardButton('Информатика', callback_data='gradeИнформатика'),
    types.InlineKeyboardButton('Русский язык', callback_data='gradeРусский язык'),
    types.InlineKeyboardButton('Литература', callback_data='gradeЛитература'),
    types.InlineKeyboardButton('Биология', callback_data='gradeБиология'),
    types.InlineKeyboardButton('Химия', callback_data='gradeХимия'),
    types.InlineKeyboardButton('История', callback_data='gradeИстория'),
    types.InlineKeyboardButton('Обществознание', callback_data='gradeОбществознание'),
    types.InlineKeyboardButton('Английский', callback_data='gradeАнглийский'),
    types.InlineKeyboardButton('Астрономия', callback_data='gradeАстрономия'),
    types.InlineKeyboardButton('ОБЖ', callback_data='gradeОБЖ'),
    types.InlineKeyboardButton('Физкультура', callback_data='gradeФизкультура'),
).row(
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

back_to_schedule = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад в меню", callback_data="schedule")
)

en_group = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('Ольга Ивановна', callback_data='group_ОИ'),
    types.InlineKeyboardButton('Ирина Станиславовна', callback_data='group_ИС'),
)

info_group = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('Елена Николаевна', callback_data='group_ЕН'),
    types.InlineKeyboardButton('Ирина Вадимовна', callback_data='group_ИВ'),
)

file_exist = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Да", callback_data="file_exists"),
    types.InlineKeyboardButton("Нет", callback_data="file_not_exists"),
)

back_to_marks_subjects = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('Назад к предметам', callback_data='marks')
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
        try:
            day_num = datetime.datetime(2023, int(date[0].split('.')[1]), int(date[0].split('.')[0])).weekday()
        except:
            pass
        date_markup.insert(
            types.InlineKeyboardButton(f'{weekdays[day_num]} - {date[0]}', callback_data=f"gettasklist_{date[0]}")
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
