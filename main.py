import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from pathlib import Path
import datetime
import shutil


class ClientState(StatesGroup):
    START = State()
    ADMIN = State()
    NEW_TASK_DATE = State()
    NEW_TASK_SUBJECT = State()
    NEW_TASK_FILE = State()
    NEW_TASK_FINISH = State()
    MARKS_IMPORT = State()
    CHANGERATE_NUMBER = State()
    CHANGERATE_DESC = State()
    SENDALL = State()
    SUPPORT = State()
    ADD_MARKS = State()


import os
import config as cfg
import markups as nav
import helpers as help
from dbshka import Database

storage = RedisStorage2()
bot = Bot(token=cfg.TOKEN_TEST)
dp = Dispatcher(bot, storage=storage)
db = Database(os.path.abspath(cfg.db_file))
db.create_tables()
flag = 0


async def delete_msg(message, count):
    try:
        for i in range(count):
            await bot.delete_message(message.chat.id, message.message_id - i)
    except:
        pass


def smart_sort(mass: list):
    mass.sort(key=lambda x: x[0].split(".")[0])
    mass.sort(key=lambda x: x[0].split(".")[1])
    return mass


def is_correct(text):
    text_split = text.split()
    if len(text_split) > 3:
        return "Вы ввели лишний пробел. Попробуйте еще раз"
    elif not help.check_subject(text_split[0]):
        subj = "\n".join(help.subjects)
        return f"Проверьте правильность предмета. Пишите пожалуйста с большой буквы. Предметы:\n{subj}"
    elif "." not in text_split[1]:
        return "Проверьте правильность даты. Пишите пожалуйста через точку, например, 11.11"
    else:
        try:
            int(text_split[2])
        except:
            return "Проверьте правильность оценки. Вводите только числа"
    return True


async def err(e, chat):
    print(e)
    await bot.send_message(chat, "Что-то пошло не так")


@dp.message_handler(commands=["clearmarks"], state=ClientState.all_states)
async def start(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 1)
        if db.get_user(chatid)[4] != "user":
            all_students = db.get_all_users()
            help.nullify_marks(all_students)
    except Exception as e:
        await err(e, chatid)


# Старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        if chatid == cfg.teacher:
            await bot.send_message(
                chatid,
                "Здравствуйте, Татьяна Алексеевна",
                reply_markup=nav.get_admin_menu("teacher"),
            )
            await state.set_state(ClientState.ADMIN)
            return
        if not db.user_exists(chatid):
            await bot.send_message(
                chatid,
                f"Ты не прошел предварительную регистрацию, обратись к админу - {cfg.admin_nick}",
            )
            return
        if db.get_user(chatid)[3] == "1":
            await bot.send_message(
                chatid,
                "К сожалению вы получили блокировку.",
            )
            return
        await bot.send_message(
            chatid,
            f"Добро пожаловать в наш электронный дневкик, {db.get_user(chatid)[1] if db.get_user(chatid)[1] != 'Виктория Горюнова' else 'Вика Морозова-Дементьева-<s>Куст</s>'}",
            reply_markup=nav.menu,
            parse_mode="HTML",
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        await err(e, chatid)


# Админская часть
@dp.message_handler(commands=["admin"], state=ClientState.all_states)
async def admin(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        if db.get_user(chatid)[4] != "user":
            await bot.send_message(
                chatid,
                "Админ пришел, всем к ногам",
                reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
            )
            await state.set_state(ClientState.ADMIN)
    except Exception as e:
        await err(e, chatid)


@dp.callback_query_handler(state=ClientState.ADMIN)
async def admin_callback(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query_id=call.id)
        chatid = call.message.chat.id
        messageid = call.message.message_id
        if call.data == "marks":
            students = db.get_all_users()
            await bot.edit_message_text(
                "Выбери ученика",
                chatid,
                messageid,
                reply_markup=nav.get_students_page(0, students, [], "getmarks"),
            )
        elif call.data == "edit_marks":
            students = db.get_all_users()
            await bot.edit_message_text(
                "Выбери ученика",
                chatid,
                messageid,
                reply_markup=nav.get_students_page(0, students, [], "editmarks"),
            )
        elif call.data == "add_marks":
            await bot.edit_message_text(
                "Присылай оценки в формате:\nПредмет Дата Оценка\nПример: Английский 11.11 5\nКак закончишь, пришли '-' без кавычек",
                chatid,
                messageid,
            )
            await state.update_data(add_marks_message=messageid)
            await state.set_state(ClientState.ADD_MARKS)
        elif call.data == "del_marks":
            await bot.edit_message_text(
                "Выбери предмет",
                chatid,
                messageid,
                reply_markup=nav.get_subjects_markup("delmarks"),
            )
        elif call.data == "edit_hometask":
            await bot.edit_message_text(
                "Выбери действие", chatid, messageid, reply_markup=nav.admin_task
            )
        elif call.data == "marks_import":
            await bot.edit_message_text(
                "Выбери действие", chatid, messageid, reply_markup=nav.marks_choose
            )
        elif call.data == "sendall":
            await bot.edit_message_text(
                'Напиши текст для рассылки или отправь "-" для отмены',
                chatid,
                messageid,
            )
            await state.set_state(ClientState.SENDALL)
        elif call.data == "schedule":
            await bot.edit_message_text(
                "Выберите день", chatid, messageid, reply_markup=nav.schedule
            )
        elif call.data == "add_hometask":
            await state.update_data(doc_path=[])
            await state.update_data(group="")
            await bot.edit_message_text(
                "Напиши дату в формате 27.10 обязательно с точкой!!!", chatid, messageid
            )
            await state.set_state(ClientState.NEW_TASK_DATE)
        elif call.data == "del_hometask":
            all_dates = smart_sort(list(set(db.get_all_dates())))
            if len(all_dates) == 0:
                await bot.edit_message_text(
                    "Пока что нет домашнего задания",
                    chatid,
                    messageid,
                    reply_markup=nav.back_to_menu,
                )
                return
            await bot.edit_message_text(
                "Выбери день",
                chatid,
                messageid,
                reply_markup=nav.get_dates_markup(all_dates),
            )
        elif call.data == "support":
            await bot.edit_message_text(
                'Напишите ниже ваши пожелания или возникшие ошибки. Для отмены отправьте "-" без кавычек',
                chatid,
                messageid,
            )
            await state.set_state(ClientState.SUPPORT)
        elif call.data == "bansystem":
            await bot.edit_message_text(
                "Выбери ученика",
                chatid,
                messageid,
                reply_markup=nav.get_students_page(
                    0, db.get_all_users(), [], "bansyschoose"
                ),
            )
        elif call.data == "file_exists":
            await delete_msg(call.message, 1)
            await bot.send_message(
                chatid,
                'Пришли один или несколько файлов без лишнего текста и т.п. Как закончишь, напиши "-" без кавычек',
            )
            await state.set_state(ClientState.NEW_TASK_FILE)
        elif call.data == "file_not_exists":
            await delete_msg(call.message, 1)
            await bot.send_message(chatid, "Напиши текст дз")
            await state.set_state(ClientState.NEW_TASK_FINISH)
            await state.update_data(doc_path=["None"])
        elif call.data == "back_to_menu":
            await bot.edit_message_text(
                "Вот ваше меню господин админ",
                chatid,
                messageid,
                reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
            )
        elif call.data == "edit_socialrate":
            students = db.get_all_users()
            rates = db.get_all_rates()
            await bot.edit_message_text(
                "Выбери ученика",
                chatid,
                messageid,
                reply_markup=nav.get_students_page(0, students, rates, "changerate"),
            )
        elif call.data == "back_to_start":
            await bot.edit_message_text(
                "Удачи в этом суровом мире", chatid, messageid, reply_markup=nav.menu
            )
            await state.set_state(ClientState.START)
        elif "page" in call.data:
            students = db.get_all_users()
            rates = db.get_all_rates()
            await bot.edit_message_reply_markup(
                chatid,
                messageid,
                reply_markup=nav.get_students_page(
                    int(call.data.split()[1]), students, rates, call.data.split()[2]
                ),
            )
        elif "bansyschoose" in call.data:
            student = call.data.split("_")[1]
            await bot.edit_message_text(
                "Выбери действие",
                chatid,
                messageid,
                reply_markup=nav.get_bansystem_markup(student),
            )
        elif "delmarks" in call.data:
            state_data = await state.get_data()
            student_lastname = state_data["edit_marks_student"]
            if len(call.data.split("_")) == 3:
                data_split = call.data.split("_")
                subject = state_data["del_mark_subject"]
                # print(
                #     student_lastname,
                #     subject,
                #     data_split[1],
                #     int(call.data.split("_")[2]),
                # )
                help.delete_mark(
                    student_lastname,
                    subject,
                    data_split[1],
                    int(data_split[2]),
                )
            else:
                subject = call.data[8:]
                await state.update_data(del_mark_subject=subject)
            student_marks = help.get_marks_mass(student_lastname)[subject]
            await bot.edit_message_text(
                "Выбери оценку, которую хочешь удалить",
                chatid,
                messageid,
                reply_markup=nav.get_del_marks_markup(student_marks),
            )
        elif "editmarks" in call.data:
            if len(call.data.split("_")) != 1:
                lastname = call.data.split("_")[1]
                await state.update_data(edit_marks_student=call.data.split("_")[1])
            else:
                state_data = await state.get_data()
                lastname = state_data["edit_marks_student"]
            await bot.edit_message_text(
                f"Что вы хотите сделать с оценками ученика: {lastname}",
                chatid,
                messageid,
                reply_markup=nav.edit_marks_choose,
            )
        elif "ban" in call.data:
            data_split = call.data.split("_")
            user_id = db.get_id_from_lastname(data_split[1])
            if data_split[0] == "ban":
                db.ban(user_id)
                await bot.edit_message_text(
                    "Ученик успешно забанен",
                    chatid,
                    messageid,
                    reply_markup=nav.back_to_menu,
                )
            else:
                db.unban(user_id)
                await bot.edit_message_text(
                    "Ученик успешно разбанен",
                    chatid,
                    messageid,
                    reply_markup=nav.back_to_menu,
                )
        elif "getmarks_" in call.data:
            data = call.data.split("_")
            all_marks = help.get_marks_mass(data[1])
            marks_text = f"<b>{data[1]}</b>\n"
            for subject in all_marks:
                student_marks = []
                for mark in all_marks[subject]:
                    student_marks.append(list(mark.values())[0])
                student_marks_str = map(str, student_marks)
                marks_text += f'<i>{subject}:</i> {"Нет оценок" if len(student_marks) == 0 else " ".join(student_marks_str)} - <b>{0 if len(student_marks) == 0 else round(sum(student_marks)/len(student_marks), 2)}</b>\n'
            await bot.edit_message_text(
                marks_text,
                chatid,
                messageid,
                parse_mode="HTML",
                reply_markup=nav.back_to_marks_students,
            )

        elif "changerate_" in call.data:
            await state.update_data(change_student=call.data.split("_")[1])
            await bot.edit_message_text(
                "Напиши насколько ты хочешь изменить рейтинг этого ученика. Например, +3 или -5, знак обязателен",
                chatid,
                messageid,
            )
            await state.set_state(ClientState.CHANGERATE_NUMBER)
        elif "importmarks" in call.data:
            await state.update_data(form_type=call.data.split("_")[1])
            await bot.edit_message_text(
                "Пришли файл в формате '.docx' или введи '-' для отмены.",
                chatid,
                messageid,
            )
            await state.set_state(ClientState.MARKS_IMPORT)
        elif "group" in call.data:
            await delete_msg(call.message, 1)
            await state.update_data(group=call.data.split("_")[1])
            await bot.send_message(
                chatid, "Добавить файл к заданию?", reply_markup=nav.file_exist
            )
        elif "gettasklist" in call.data:
            date = call.data[12:]
            task_list = db.get_date_tasks(date)
            await bot.edit_message_text(
                "Что будем делать?",
                chatid,
                messageid,
                reply_markup=nav.get_del_task_markup(task_list, date),
            )
        elif "deltask" in call.data:
            task_info = call.data.split("_")
            db.del_task(task_info[1], task_info[2])
            all_task = db.get_date_tasks(task_info[1])
            if len(all_task) == 0:
                await bot.edit_message_text(
                    "На этот день больше нет домашнего задания",
                    chatid,
                    messageid,
                    reply_markup=nav.admin_back_to_dates,
                )
                return
            await bot.edit_message_reply_markup(
                chatid,
                messageid,
                reply_markup=nav.get_del_task_markup(all_task, task_info[1]),
            )
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.ADD_MARKS)
async def changerate_number(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    try:
        state_data = await state.get_data()
        await delete_msg(message, 1)
        if message.text == "-":
            await delete_msg(message, 1)
            await bot.delete_message(chatid, state_data["add_marks_message"])
            await bot.send_message(
                chatid,
                f"Что вы хотите сделать с оценками ученика: {state_data['edit_marks_student']}",
                reply_markup=nav.edit_marks_choose,
            )
            await state.set_state(ClientState.ADMIN)
            return
        elif is_correct(message.text) != True:
            msg = await bot.send_message(chatid, is_correct(message.text))
            time.sleep(5)
            await bot.delete_message(chatid, msg.message_id)
            return
        data = message.text.split()
        help.insert_marks(
            state_data["edit_marks_student"], data[0], data[1], int(data[2])
        )
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.SENDALL)
async def sendall(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await state.set_state(ClientState.ADMIN)
        await delete_msg(message, 2)
        if message.text == "-":
            await bot.send_message(
                chatid,
                "Вот ваше меню господин",
                reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
            )
            return
        all_users = db.get_all_users()
        for user in all_users:
            chat_id = user[0]
            try:
                if user[1].split()[1] != "Новиков":
                    await bot.send_message(chat_id, message.text, reply_markup=nav.hide)
            except Exception as e:
                await bot.send_message(
                    chatid,
                    f"Сообщение не отправлено пользователю: {user[1]}\nПо причине: {e}",
                    reply_markup=nav.hide,
                )
        await bot.send_message(
            chatid,
            "Вот ваше меню господин",
            reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
        )

    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.CHANGERATE_NUMBER)
async def changerate_number(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        if not message.text.startswith("+") and not message.text.startswith("-"):
            await bot.send_message(chatid, 'Я же просил начинать со знака "+" или "-"')
            return
        try:
            int(message.text[1:])
        except:
            await bot.send_message(chatid, "Ты ввел не число")
            return
        await state.update_data(change_number=message.text)
        await bot.send_message(
            chatid,
            "За что его так?"
            if message.text[0] == "-"
            else "И что же такого хорошего он сделал?",
        )
        await state.set_state(ClientState.CHANGERATE_DESC)
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.CHANGERATE_DESC)
async def changerate_desc(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        state_data = await state.get_data()
        change = state_data["change_number"]
        lastname = state_data["change_student"]
        day = ".".join(str(datetime.date.today()).split("-")[1:][::-1])
        note = f"{day}_{change}_{message.text}"
        rate = change[1:] if change[0] == "+" else int(change[1:]) * -1
        db.change_rate(lastname, rate, note)
        await state.set_state(ClientState.ADMIN)
        await bot.send_message(
            chatid,
            "Вот ваше меню господин",
            reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
        )
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.MARKS_IMPORT, content_types=["document", "text"])
async def marks_import(message: types.Message, state: FSMContext):
    # try:
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.content_type == "text":
        if message.text == "-":
            await state.set_state(ClientState.ADMIN)
            await bot.send_message(
                chatid,
                "Вот ваше меню господин",
                reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
            )
            return
    await state.set_state(ClientState.ADMIN)
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    shutil.rmtree("convert/")
    os.mkdir("convert/")
    with open("convert/interim_word.docx", "wb") as new_file:
        new_file.write(downloaded_file.getvalue())
    help.convert_to_json()
    state_data = await state.get_data()
    help.form_marks_mass(state_data["form_type"])
    await bot.send_message(
        chatid,
        "Вот ваше меню господин",
        reply_markup=nav.get_admin_menu(db.get_user(chatid)[4]),
    )


# except Exception as e:
#     await err(e, chatid)
#     print("marks_import")


@dp.message_handler(state=ClientState.NEW_TASK_DATE)
async def new_task_date(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        if not "." in message.text:
            await bot.send_message(
                chatid,
                "Неверный формат даты. Обязательно вводить через точку, например 02.01",
            )
            return
        await state.update_data(date=message.text)
        await bot.send_message(chatid, "По какому предмету это дз?")
        await state.set_state(ClientState.NEW_TASK_SUBJECT)
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.NEW_TASK_SUBJECT)
async def new_task_subject(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        if not help.check_subject(message.text):
            await bot.send_message(
                chatid,
                "Такого предмета у нас нет. Вводи, пожалуйста, с большой буквы, например, Алгебра",
            )
            return
        await state.update_data(subject=message.text)
        if message.text == "Английский" or message.text == "Информатика":
            markup = nav.en_group if message.text == "Английский" else nav.info_group
            await bot.send_message(chatid, "Какой группе это дз?", reply_markup=markup)
            await state.set_state(ClientState.ADMIN)
            return
        await bot.send_message(
            chatid, "Добавить файл к заданию?", reply_markup=nav.file_exist
        )
        await state.set_state(ClientState.ADMIN)
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(
    content_types=["photo", "document", "text"], state=ClientState.NEW_TASK_FILE
)
async def new_task_file(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        Path(f"hometask_docs/").mkdir(parents=True, exist_ok=True)
        if message.content_type == "photo":
            file_info = await bot.get_file(
                message.photo[len(message.photo) - 1].file_id
            )
            downloaded_file = await bot.download_file(file_info.file_path)
            src = f"hometask_docs/" + file_info.file_path.replace("photos/", "")
            state_data = await state.get_data()
            new_doc_path = state_data["doc_path"]
            new_doc_path.append(file_info.file_path.replace("photos/", ""))
            await state.update_data(doc_path=new_doc_path)
            with open(src, "wb") as new_file:
                new_file.write(downloaded_file.getvalue())
            await bot.send_message(chatid, "Успешно добавлено")
        elif message.content_type == "document":
            file_info = await bot.get_file(message.document.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            src = f"hometask_docs/" + message.document.file_name
            state_data = await state.get_data()
            new_doc_path = state_data["doc_path"]
            new_doc_path.append(message.document.file_name)
            await state.update_data(doc_path=new_doc_path)
            with open(src, "wb") as new_file:
                new_file.write(downloaded_file.getvalue())
            await bot.send_message(chatid, "Успешно добавлено")
        elif message.text == "-":
            await bot.send_message(chatid, "Напиши текст дз")
            await state.set_state(ClientState.NEW_TASK_FINISH)
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.NEW_TASK_FINISH)
async def new_task_finish(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        state_data = await state.get_data()
        await delete_msg(message, (len(state_data["doc_path"]) * 2))
        task_text = message.text
        if state_data["group"] != "":
            task_text = f'{state_data["group"]} {message.text}'
        db.add_task(
            state_data["date"], state_data["subject"], task_text, state_data["doc_path"]
        )
        await bot.send_message(
            chatid, "Успешно добавлено", reply_markup=nav.back_to_menu
        )
        await state.set_state(ClientState.ADMIN)
    except Exception as e:
        await err(e, chatid)


# Часть обычных смертных
@dp.callback_query_handler(state=ClientState.all_states)
async def callback(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query_id=call.id)
        chatid = call.message.chat.id
        messageid = call.message.message_id
        if db.get_user(chatid)[3] == "1":
            await bot.edit_message_text("Вы получили блокировку.", chatid, messageid)
            return
        if call.data == "marks":
            all_marks = help.get_marks_mass(db.get_user(chatid)[1].split()[1])
            marks_text = f"<b>Ваши оценки</b>\n"
            for subject in all_marks:
                student_marks = []
                for mark in all_marks[subject]:
                    student_marks.append(list(mark.values())[0])
                student_marks_str = map(str, student_marks)
                marks_text += f'<i>{subject}:</i> <b>[{0 if len(student_marks) == 0 else round(sum(student_marks)/len(student_marks), 2)}]</b> - {"Нет оценок" if len(student_marks) == 0 else " ".join(student_marks_str)}\n'
            await bot.edit_message_text(
                marks_text,
                chatid,
                messageid,
                parse_mode="HTML",
                reply_markup=nav.all_marks,
            )
        elif call.data == "marks_with_dates":
            await bot.edit_message_text(
                "Выберите предмет",
                chatid,
                messageid,
                reply_markup=nav.get_subjects_markup("grade"),
            )
        elif call.data == "support":
            await bot.edit_message_text(
                'Напишите ниже ваши пожелания или возникшие ошибки. Для отмены отправьте "-" без кавычек',
                chatid,
                messageid,
            )
            await state.set_state(ClientState.SUPPORT)
        elif call.data == "hometask":
            all_tasks = smart_sort(list(set(db.get_all_dates())))
            if len(all_tasks) == 0:
                await bot.edit_message_text(
                    "Пока что нет домашнего задания",
                    chatid,
                    messageid,
                    reply_markup=nav.back_to_menu,
                )
                return
            await bot.edit_message_text(
                "Выберите дату",
                chatid,
                messageid,
                reply_markup=nav.get_dates_markup(all_tasks),
            )
        elif call.data == "socialrate":
            user_lastname = db.get_user(chatid)[1].split()[1]
            rate_text = f"Лучшая система оценивания на свете\n<b>Рейтинг:</b> <i>{db.get_rate(user_lastname)[0]}</i>"
            await bot.edit_message_text(
                rate_text,
                chatid,
                messageid,
                reply_markup=nav.rating_history,
                parse_mode="HTML",
            )
        elif call.data == "rating_history":
            user_lastname = db.get_user(chatid)[1].split()[1]
            history_mass = db.get_history(user_lastname)[0].split("/")
            history_mass.pop(len(history_mass) - 1)
            history_mass = history_mass[::-1]
            history_text = "Все изменения вашего социального рейтинга:\n"
            for case in history_mass:
                case_data = case.split("_")
                history_text += f"● {case_data[0]}: Изменен на {case_data[1]}. Причина: {case_data[2]}\n"
            await bot.edit_message_text(
                history_text, chatid, messageid, reply_markup=nav.back_to_socialrate
            )
        elif call.data == "schedule":
            await bot.edit_message_text(
                "Выберите день", chatid, messageid, reply_markup=nav.schedule
            )
        elif call.data == "back_to_dates":
            all_tasks = smart_sort(list(set(db.get_all_dates())))
            await bot.edit_message_text(
                "Выберите дату",
                chatid,
                messageid,
                reply_markup=nav.get_dates_markup(all_tasks),
            )
        elif call.data == "back_to_menu":
            await bot.edit_message_text(
                f"Добро пожаловать в меню, {db.get_user(chatid)[2] if db.get_user(chatid)[1] != 'Виктория Горюнова' else 'Вика Морозова-Дементьева-Куст'}",
                chatid,
                messageid,
                reply_markup=nav.menu,
            )
        elif call.data == "hide":
            await delete_msg(call.message, 1)
        elif call.data == "get_all_marks":
            all_marks = help.get_marks_mass(db.get_user(chatid)[1].split()[1])
            marks_text = f"<b>Ваши оценки</b>\n"
            for subject in all_marks:
                student_marks = all_marks[subject]
                student_marks_str = map(str, student_marks)
                marks_text += f'<i>{subject}:</i> <b>{0 if len(student_marks) == 0 else round(sum(student_marks)/len(student_marks), 2)}</b> - {"Нет оценок" if len(student_marks) == 0 else " ".join(student_marks_str)}\n'
            await bot.edit_message_text(
                marks_text,
                chatid,
                messageid,
                parse_mode="HTML",
                reply_markup=nav.back_to_marks_subjects,
            )
        elif "grade" in call.data:
            subject = call.data[5:]
            subject_marks = help.get_marks_mass(db.get_user(chatid)[1].split()[1])[
                subject
            ]
            marks_text = f"<b>{subject}</b>\n<code>"
            if len(subject_marks) == 0:
                marks_text += "Нет оценок"
            for mark in subject_marks:
                mark_key = list(mark.keys())[0]
                data_split = mark_key.split(".")
                day_num = datetime.datetime(
                    2023, int(data_split[1]), int(data_split[0])
                ).weekday()
                marks_text += f"{help.weekdays_short[day_num]} {data_split[0]} {help.months_names[int(data_split[1]) - 1][:-1] + 'я'} - {mark[mark_key]}\n"
            marks_text += "</code>"
            await bot.edit_message_text(
                marks_text,
                chatid,
                messageid,
                parse_mode="HTML",
                reply_markup=nav.back_to_marks_subjects,
            )
        elif "day" in call.data:
            desired_day = call.data[3:]
            day_lst = help.get_schedule(flag)[desired_day]
            timestable = help.get_timestable(desired_day)
            schedule_str = ""
            for i in range(len(day_lst)):
                schedule_str += f'<i>{day_lst[i]}:</i> {timestable[i if desired_day != "Суббота" else i+1]}\n'
            await bot.edit_message_text(
                f"<b>{desired_day}:</b> \n{schedule_str}",
                chatid,
                messageid,
                parse_mode="HTML",
                reply_markup=nav.back_to_schedule,
            )
        elif "file" in call.data:
            data = call.data.split("_")
            files = db.get_subject_files(data[1], data[2])[0][1:].split("|")
            for f in files:
                try:
                    file = open(f"hometask_docs/{f}", "rb")
                    await bot.send_photo(chatid, file, reply_markup=nav.hide)
                except:
                    file = open(f"hometask_docs/{f}", "rb")
                    await bot.send_document(chatid, file, reply_markup=nav.hide)
        elif "gettasklist" in call.data:
            date = call.data[12:]
            day = datetime.datetime(
                2023, int(date.split(".")[1]), int(date.split(".")[0])
            )
            task_list = db.get_date_tasks(date)
            task_text = f"{help.weekdays[day.weekday()]} - {date}\n"
            second_name = db.get_user(chatid)[1].split()[1]
            for task in task_list:
                if task[1] == "Английский":
                    if task[2].startswith("ОИ") and second_name in help.group_OI:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                    elif task[2].startswith("ИС") and not second_name in help.group_OI:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                elif task[1] == "Информатика":
                    if task[2].startswith("ЕН") and second_name in help.group_EN:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                    elif task[2].startswith("ИВ") and not second_name in help.group_EN:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                else:
                    task_text += f"<i><b>{task[1]}</b></i>: {task[2]}\n\n"
            await bot.edit_message_text(
                task_text,
                chatid,
                messageid,
                reply_markup=nav.get_files_markup(task_list),
                parse_mode="HTML",
            )
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(state=ClientState.SUPPORT)
async def new_task_finish(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
        if db.get_user(chatid)[3] == "1":
            await bot.send_message(chatid, "Вы получили блокировку.")
            return
        if message.text == "-":
            if chatid == cfg.teacher:
                await bot.send_message(
                    chatid,
                    "Здравствуйте, Татьяна Алексеевна",
                    reply_markup=nav.get_admin_menu("teacher"),
                )
                await state.set_state(ClientState.ADMIN)
            await bot.send_message(
                chatid, "Так уж и быть, держи меню", reply_markup=nav.menu
            )
            await state.set_state(ClientState.START)
            return
        await bot.send_message(
            cfg.glav_admin,
            f"Новое обращение от {db.get_user(chatid)[1]}:\n{message.text}",
            reply_markup=nav.hide,
        )
        if chatid == cfg.teacher:
            await bot.send_message(
                chatid,
                "Спасибо за обращение, очень ответственный админ постарается рассмотреть его в ближайшее время",
                reply_markup=nav.get_admin_menu("teacher"),
            )
            await state.set_state(ClientState.ADMIN)
        await bot.send_message(
            chatid,
            "Спасибо за обращение, очень ответственный админ постарается рассмотреть его в ближайшее время",
            reply_markup=nav.menu,
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(content_types=["text"], state=ClientState.all_states)
async def text(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 1)
        if db.get_user(chatid)[3] == "1":
            await bot.send_message(chatid, "Вы получили блокировку.")
            return
        await bot.send_message(
            chatid,
            "Не знаю что ты хотел сделать, держи меню",
            reply_markup=nav.menu,
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(content_types=["text"])
async def text(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 1)
        await bot.send_message(
            message.chat.id,
            "Бота видимо перезапустили, поэтому напиши /start пожалуйста",
        )
    except Exception as e:
        await err(e, chatid)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
