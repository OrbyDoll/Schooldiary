import asposecells
import jpype

jpype.startJVM()
from asposecells.api import Workbook
import datetime
import json
import math
import mammoth


weekdays = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]
group_OI = [
    "Хазин",
    "Ряжских",
    "Мовсесян",
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


def check_subject(subject):
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
            new_subject_marks = new_marks[student][subject_name]
            for mark in new_subject_marks:
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
    all_marks = {}
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
                    for grade in str(subject[mark]).replace("\n", "").split():
                        try:
                            # Отсеивание не чисел
                            marks.append(int(grade))
                        except:
                            pass
            key_name = subject[keys[-1]]
            if subject[keys[-1]] == "Основы безопасности жизнедеятельности":
                key_name = "ОБЖ"
            elif subject[keys[-1]] == "Иностранный язык: Английский":
                key_name = "Английский"
            elif subject[keys[-1]] == "Физическая культура":
                key_name = "Физкультура"
            student_marks[key_name] = marks
        all_marks[student[0]["Ученик"].split()[0]] = student_marks
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
    return old_marks[lastname]
