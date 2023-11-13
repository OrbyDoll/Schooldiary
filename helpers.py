import asposecells
import jpype

jpype.startJVM()
from asposecells.api import Workbook
import datetime
import json
import math
import mammoth


months_names = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]
weekdays = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]
weekdays_short = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
group_OI = [
    "Хазин",
    "Ряжских",
    "Мовсесян",
    "Данилова",
    "Ширнин",
    "Горюнова",
    "Митин",
    "Мягков",
    "Благов",
    "Новиков",
    "Хаитова",
    "Смирнов",
    "Карасев",
]
group_EN = [
    "Хазин",
    "Чурилов",
    "Мовсесян",
    "Ширнин",
    "Данилова",
    "Ляпина",
    "Штарев",
    "Лаврентьев",
    "Кудрявцев",
    "Ватутина",
    "Карасев",
]
mark_subjects = [
    "Русский",
    "Математика",
    "Литература",
    "Физика",
    "История",
    "Обществознание",
    "Биология",
    "Химия",
    "ОБЖ",
    "Английский",
    "Астрономия",
    "Информатика",
    "Физкультура",
]


def func_chunk(lst, part_len):
    for elem in range(0, len(lst), part_len):
        part = lst[elem : part_len + elem]

        if len(part) < part_len:
            part = part + [None for y in range(part_len - len(part))]
        yield part


subjects = [
    "Русский",
    "Алгебра",
    "Геометрия",
    "Литература",
    "Физика",
    "История",
    "Обществознание",
    "Биология",
    "Химия",
    "ОБЖ",
    "Английский",
    "Астрономия",
    "Информатика",
    "Физкультура",
    "ЕГЭ Математика",
]


def check_subject(subject):
    if subject in subjects:
        return True
    return False


def get_schedule(flag):
    now = datetime.datetime.today()
    first_saturday = datetime.datetime(2023, 9, 2)
    distinction = math.ceil((now - first_saturday).days / 7)
    if now.isoweekday() == 7:
        distinction += 1
    schedule = {
        "Понедельник": [
            "Разговоры о важном",
            "Алгебра",
            "Алгебра",
            "История",
            "История",
            "Английский",
            "Физика",
            "ЕГЭ Математика",
        ],
        "Вторник": [
            "Информатика",
            "Информатика",
            "Геометрия",
            "Геометрия",
            "Химия",
            "Химия",
            "Классный час",
        ],
        "Среда": ["Ко второму", "Астрономия", "Физика", "Физика", "Английский", "ОБЖ"],
        "Четверг": [
            "Физика",
            "Физика",
            "Обществознание",
            "Обществознание",
            "Литература",
            "Английский",
        ],
        "Пятница": [
            "Биология",
            "Литература",
            "Алгебра",
            "Алгебра",
            "Информатика",
            "Информатика",
            "Литература",
        ],
        "Суббота": [
            "Физкульура",
            "Физкульура",
            "Алгебра" if distinction % 2 == 1 * flag else "Геометрия",
            "Алгебра" if distinction % 2 == 1 * flag else "Геометрия",
            "Биология",
            "Русский",
        ],
    }
    return schedule


def get_timestable(weekday):
    if weekday == "Понедельник" or weekday == "Суббота":
        return [
            "8:00 - 8:45",
            "8:45 - 9:25",
            "9:35 - 10:15",
            "10:30 - 11:10",
            "11:25 - 12:05",
            "12:20 - 13:00",
            "13:10 - 13:50",
            "14:05 - 14:45",
        ]
    return [
        "8:30 - 9:15",
        "9:25 - 10:10",
        "10:25 - 11:10",
        "11:25 - 12:10",
        "12:25 - 13:10",
        "13:20 - 14:05",
        "14:15 - 14:55",
    ]


def convert_to_json():
    with open("convert/interim_word.docx", "rb") as doc_file:
        doc_to_html = mammoth.convert_to_html(doc_file)
    with open("convert/interim_html.html", "w", encoding="utf-8") as htmlfile:
        htmlfile.write(doc_to_html.value)
    book = Workbook("convert/interim_html.html")
    book.save("convert/interim_result.json")


def add_marks(old_marks, new_marks):
    for student in old_marks:
        subjects = old_marks[student]
        for subject_name in subjects:
            prev_subject_marks = old_marks[student][subject_name]
            new_subject_marks = new_marks[student][subject_name]
            for mark in new_subject_marks:
                if not mark in prev_subject_marks:
                    subjects[subject_name].append(mark)
    return old_marks


def form_marks_mass(type):
    with open("convert/interim_result.json", encoding="utf-8") as json_file:
        raw_mass = json.load(json_file)
    for i in range(raw_mass.count(None)):
        raw_mass.remove(None)
    for obj in raw_mass:
        if list(obj.items())[0][1] == "Классный час":
            raw_mass.remove(obj)
    extra_key = list(raw_mass[0].keys())[0]
    divided_mass = list(func_chunk(raw_mass, 16))
    date_guide = {}
    all_marks = {}

    # Распределение дат по колонкам
    months_column = divided_mass[0][1]
    months_keys = list(months_column.keys())
    for date in divided_mass[0][2]:
        # print(int(date[6:]), int(months_keys[len(months_column) - 1][6:]))
        if len(months_column) == 1:
            unformatted_date_month = (
                months_names.index(months_column[months_keys[0]]) + 1
            )
        elif int(date[6:]) >= int(months_keys[len(months_column) - 1][6:]):
            unformatted_date_month = (
                months_names.index(months_column[months_keys[len(months_column) - 1]])
                + 1
            )
        else:
            keys = list(map(lambda x: int(x[6:]), list(months_keys)))
            ranges = [range(keys[i - 1], keys[i]) for i in range(1, len(keys))]
            for rng in ranges:
                if int(date[6:]) in rng:
                    unformatted_date_month = (
                        months_names.index(
                            months_column[months_keys[ranges.index(rng)]]
                        )
                        + 1
                    )
        date_month = (
            unformatted_date_month
            if len(str(unformatted_date_month)) == 2
            else "0" + str(unformatted_date_month)
        )
        day = (
            divided_mass[0][2][date]
            if len(str(divided_mass[0][2][date])) == 2
            else "0" + str(divided_mass[0][2][date])
        )
        date_guide[date] = f"{day}.{date_month}"

    # Формирование словаря - ученик : [{Предмет : Оценка}, ...]
    for student in divided_mass:
        student[0]["Ученик"] = student[0].pop(extra_key)
        for data in student:
            if extra_key in data:
                data["Предмет"] = data.pop(extra_key)
        student_marks = {}
        for subject in student[3:]:
            keys = list(subject.keys())
            marks = []
            for mark in subject:
                if "Column" in mark:
                    for grade in str(subject[mark]).replace("\n", " ").split():
                        try:
                            # Отсеивание не чисел
                            marks.append({date_guide[mark]: int(grade)})
                        except:
                            pass
            key_name = subject[keys[-1]]
            if subject[keys[-1]] == "Основы безопасности жизнедеятельности":
                key_name = "ОБЖ"
            elif subject[keys[-1]] == "Иностранный язык: Английский":
                key_name = "Английский"
            elif subject[keys[-1]] == "Физическая культура":
                key_name = "Физкультура"
            elif subject[keys[-1]] == "Русский язык":
                key_name = "Русский"
            student_marks[key_name] = marks
        all_marks[student[0]["Ученик"].split()[0]] = student_marks

    # Замена или добавление оценок
    if type == "replace":
        with open("final_marks.json", "w", encoding="utf-8") as main_file:
            json.dump(all_marks, main_file, ensure_ascii=False)
    elif type == "add":
        with open("final_marks.json", "r", encoding="utf-8") as main_file:
            old_marks = json.load(main_file)
        with open("final_marks.json", "w", encoding="utf-8") as main_file:
            new_marks = add_marks(old_marks, all_marks)
            json.dump(new_marks, main_file, ensure_ascii=False)


def get_marks_mass(lastname):
    with open("final_marks.json", "r", encoding="utf-8") as main_file:
        old_marks = json.load(main_file)
    if lastname == "all":
        return old_marks
    return old_marks[lastname]


def insert_marks(lastname, subject, date, mark):
    actual_marks = get_marks_mass("all")
    actual_marks[lastname][subject].append({date: mark})
    actual_marks[lastname][subject].sort(
        key=lambda x: int(list(x.keys())[0].split(".")[0])
    )
    actual_marks[lastname][subject].sort(
        key=lambda x: int(list(x.keys())[0].split(".")[1])
    )
    with open("final_marks.json", "r", encoding="utf-8") as main_file:
        old_marks = json.load(main_file)
    with open("final_marks.json", "w", encoding="utf-8") as main_file:
        json.dump(actual_marks, main_file, ensure_ascii=False)


def delete_mark(lastname, subject, date, mark):
    actual_marks = get_marks_mass("all")
    actual_marks[lastname][subject].pop(
        actual_marks[lastname][subject].index({date: mark})
    )
    with open("final_marks.json", "r", encoding="utf-8") as main_file:
        old_marks = json.load(main_file)
    with open("final_marks.json", "w", encoding="utf-8") as main_file:
        json.dump(actual_marks, main_file, ensure_ascii=False)
