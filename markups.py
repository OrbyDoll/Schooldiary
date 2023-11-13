from aiogram import types
import helpers as help
import datetime

menu = types.InlineKeyboardMarkup(row_width=3).add(
    types.InlineKeyboardButton("Оценки", callback_data="marks"),
    types.InlineKeyboardButton("Домашка", callback_data="hometask"),
    types.InlineKeyboardButton("Расписание", callback_data="schedule"),
    types.InlineKeyboardButton("Социальная активность", callback_data="socialrate"),
    types.InlineKeyboardButton("Поддержка", callback_data="support"),
)


def get_admin_menu(admin_type):
    admin_menu = types.InlineKeyboardMarkup(row_width=3)
    if admin_type == "all":
        admin_menu.add(
            types.InlineKeyboardButton("Оценки", callback_data="marks"),
            types.InlineKeyboardButton("Изменить оценки", callback_data="edit_marks"),
            types.InlineKeyboardButton("Изменить дз", callback_data="edit_hometask"),
            types.InlineKeyboardButton("Соц. рейтинг", callback_data="edit_socialrate"),
            types.InlineKeyboardButton("Импорт оценок", callback_data="marks_import"),
            types.InlineKeyboardButton("Бан система", callback_data="bansystem"),
            types.InlineKeyboardButton("Рассылка", callback_data="sendall"),
        ).row(
            types.InlineKeyboardButton(
                "Назад к обычным смертным", callback_data="back_to_start"
            )
        )
    elif admin_type == "teacher":
        admin_menu.add(
            types.InlineKeyboardButton("Оценки", callback_data="marks"),
            types.InlineKeyboardButton("Расписание", callback_data="schedule"),
        ).row(
            types.InlineKeyboardButton("Поддержка", callback_data="support"),
        )

    return admin_menu


marks_choose = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Добавить оценки", callback_data="importmarks_add"),
    types.InlineKeyboardButton("Заменить оценки", callback_data="importmarks_replace"),
)
edit_marks_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Добавить оценки", callback_data="add_marks"),
    types.InlineKeyboardButton("Удалить оценки", callback_data="del_marks"),
    types.InlineKeyboardButton("Назад к выбору учеников", callback_data="edit_marks"),
)
admin_task = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Добавить дз", callback_data="add_hometask"),
    types.InlineKeyboardButton("Удалить дз", callback_data="del_hometask"),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

schedule = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Понедельник", callback_data="dayПонедельник"),
    types.InlineKeyboardButton("Вторник", callback_data="dayВторник"),
    types.InlineKeyboardButton("Среда", callback_data="dayСреда"),
    types.InlineKeyboardButton("Четверг", callback_data="dayЧетверг"),
    types.InlineKeyboardButton("Пятница", callback_data="dayПятница"),
    types.InlineKeyboardButton("Суббота", callback_data="dayСуббота"),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)


def get_subjects_markup(type):
    return (
        types.InlineKeyboardMarkup(row_width=3)
        .add(
            types.InlineKeyboardButton("Математика", callback_data=f"{type}Математика"),
            types.InlineKeyboardButton("Физика", callback_data=f"{type}Физика"),
            types.InlineKeyboardButton(
                "Информатика", callback_data=f"{type}Информатика"
            ),
            types.InlineKeyboardButton("Русский", callback_data=f"{type}Русский"),
            types.InlineKeyboardButton("Литература", callback_data=f"{type}Литература"),
            types.InlineKeyboardButton("Биология", callback_data=f"{type}Биология"),
            types.InlineKeyboardButton("Химия", callback_data=f"{type}Химия"),
            types.InlineKeyboardButton("История", callback_data=f"{type}История"),
            types.InlineKeyboardButton(
                "Обществознание", callback_data=f"{type}Обществознание"
            ),
            types.InlineKeyboardButton("Английский", callback_data=f"{type}Английский"),
            types.InlineKeyboardButton("Астрономия", callback_data=f"{type}Астрономия"),
            types.InlineKeyboardButton("ОБЖ", callback_data=f"{type}ОБЖ"),
            types.InlineKeyboardButton(
                "Физкультура", callback_data=f"{type}Физкультура"
            ),
        )
        .row(
            types.InlineKeyboardButton("Назад ко всем оценкам", callback_data="marks")
            if type == "grade"
            else types.InlineKeyboardButton(
                "Назад к выбору действия", callback_data="editmarks"
            )
        )
    )


all_marks = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton("Оценки с датами", callback_data="marks_with_dates"),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

rating_history = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton("История изменений", callback_data="rating_history"),
    types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu"),
)

en_group = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Ольга Ивановна", callback_data="group_ОИ"),
    types.InlineKeyboardButton("Ирина Станиславовна", callback_data="group_ИС"),
)

info_group = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Елена Николаевна", callback_data="group_ЕН"),
    types.InlineKeyboardButton("Ирина Вадимовна", callback_data="group_ИВ"),
)

file_exist = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Да", callback_data="file_exists"),
    types.InlineKeyboardButton("Нет", callback_data="file_not_exists"),
)

back_to_marks_students = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад к ученикам", callback_data="marks")
)

back_to_socialrate = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад к рейтингу", callback_data="socialrate")
)

back_to_schedule = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад в меню", callback_data="schedule")
)

back_to_marks_subjects = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад к предметам", callback_data="marks_with_dates")
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
            day_num = datetime.datetime(
                2023, int(date[0].split(".")[1]), int(date[0].split(".")[0])
            ).weekday()
        except:
            pass
        date_markup.insert(
            types.InlineKeyboardButton(
                f"{help.weekdays_short[day_num]} - {date[0]}",
                callback_data=f"gettasklist_{date[0]}",
            )
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


def get_bansystem_markup(student):
    bansystem = types.InlineKeyboardMarkup(row_width=2).add(
        types.InlineKeyboardButton("Забанить", callback_data=f"ban_{student}"),
        types.InlineKeyboardButton("Разбанить", callback_data=f"unban_{student}"),
        types.InlineKeyboardButton("Назад к выбору ученика", callback_data="bansystem"),
    )
    return bansystem


def get_students_page(page, students, rates, type):
    students.sort(key=lambda x: x[1].split()[1][0])
    if len(students) == 25:
        students.pop(1)
    rates.sort(key=lambda x: x[0][0])
    item_choose = types.InlineKeyboardMarkup(row_width=1)
    if 8 * page <= 16 and 8 * page >= 0:
        for student in range(
            8 * page,
            8 * (page + 1) if 8 * (page + 1) < 24 else 24,
        ):
            text = {
                "changerate": f"{students[student][1]}: {rates[student][1] if len(rates) > 0 else ''}",
                "bansyschoose": f"{students[student][1]}: {'Забанен' if students[student][3] == '1' else 'Не забанен'}",
                "getmarks": f"{students[student][1]}",
                "editmarks": f"{students[student][1]}",
            }
            item_choose.insert(
                types.InlineKeyboardButton(
                    text=text[type],
                    callback_data=f"{type}_{students[student][1].split()[1]}",
                )
            )
        button_back = types.InlineKeyboardButton(
            text="Назад", callback_data=f"page {page - 1} {type}"
        )
        button_forward = types.InlineKeyboardButton(
            text="Вперед", callback_data=f"page {page + 1} {type}"
        )
        button_middle = types.InlineKeyboardButton(
            text=f"{page + 1}/3", callback_data="aboba"
        )
        item_choose.row(button_back, button_middle, button_forward)
        item_choose.row(
            types.InlineKeyboardButton("Назад в меню", callback_data="back_to_menu")
        )
        return item_choose
    elif 8 * page > 16:
        return get_students_page(0, students, rates, type)
    elif page < 0:
        return get_students_page(2, students, rates, type)


def get_del_marks_markup(marks):
    del_marks_markup = types.InlineKeyboardMarkup(row_width=4)
    for mark in marks:
        key = list(mark.keys())[0]
        value = list(mark.values())[0]
        del_marks_markup.insert(
            types.InlineKeyboardButton(
                f"{key} : {value}", callback_data=f"delmarks_{key}_{value}"
            )
        )
    del_marks_markup.row(
        types.InlineKeyboardButton("Назад к выбору предмета", callback_data="del_marks")
    )
    return del_marks_markup
