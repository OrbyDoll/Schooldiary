from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from pathlib import Path
import datetime

class ClientState(StatesGroup):
    START = State()
    ADMIN = State()
    NEW_TASK_DATE = State()
    NEW_TASK_SUBJECT = State()
    NEW_TASK_FILE = State()
    NEW_TASK_FINISH = State()


from os import path
import config as cfg
import markups as nav
from dbshka import Database

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN_TEST)
dp = Dispatcher(bot, storage=storage)
db = Database(path.abspath(cfg.db_file))
db.create_tables()

weekdays = ['Понедельник', "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
group_OI = ['Хазин', "Ряжский", "Мовсесян", "Ширнин", "Горюнова", "Митин", "Мягков", "Благов", "Новиков", "Хаитова", "Смирнов", "Карасев"]
group_EN = ['Хазин', "Чурилов", "Мовсесян", "Ширнин", "Данилова", "Ляпина", "Штарев", "Лаврентьев", "Кудрявцев", "Ватутина" , "Карасев"]

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
    ]
    if subject in subjects:
        return True
    return False


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


async def err(e, chat):
    print(e)
    await bot.send_message(chat, "Что-то пошло не так")


# Старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        if not db.user_exists(chatid):
            await bot.send_message(
                chatid,
                f"Ты не прошел предварительную регистрацию, обратись к админу - {cfg.admin_nick}",
            )
            return
        await bot.send_message(
            chatid, f"Привет, {message.from_user.username if db.get_user(chatid)[1] != 'Виктория Горюнова' else 'Вика Морозова-Дементьева-Куст'}", reply_markup=nav.menu
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        await err(e, chatid)


# Админская часть
@dp.message_handler(commands=["admin"], state=ClientState.all_states)
async def admin(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        if chatid == cfg.admin or chatid == cfg.glav_admin:
            await bot.send_message(
                chatid, "Админ пришел, всем к ногам", reply_markup=nav.admin_menu
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
        if call.data == "edit_marks":
            await bot.edit_message_text(
                "Мы еще этого не придумали",
                chatid,
                messageid,
                reply_markup=nav.back_to_menu,
            )
        elif call.data == "edit_hometask":
            await bot.edit_message_text(
                "Выбери действие", chatid, messageid, reply_markup=nav.admin_task
            )
        elif call.data == "add_hometask":
            await state.update_data(doc_path=[])
            await state.update_data(group='')
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
        elif call.data == "file_exists":
            await delete_msg(call.message, 1)
            await bot.send_message(
                chatid,
                'Пришли один или несколько файлов без лишнего текста и т.п. Как закончишь напиши "-" без кавычек',
            )
            await state.set_state(ClientState.NEW_TASK_FILE)
        elif call.data == "file_not_exists":
            await delete_msg(call.message, 1)
            await bot.send_message(chatid, "Напиши текст дз")
            await state.set_state(ClientState.NEW_TASK_FINISH)
            await state.update_data(doc_path=["None"])
        elif call.data == "back_to_menu":
            await bot.edit_message_text(
                "Вот ваше меню господин", chatid, messageid, reply_markup=nav.admin_menu
            )
        elif call.data == "edit_socialrate":
            await bot.edit_message_text(
                "Пока получилось сделать только фашистскую Германию...",
                chatid,
                messageid,
                reply_markup=nav.back_to_menu,
            )
        elif call.data == "back_to_start":
            await bot.edit_message_text(
                "Удачи в этом суровом мире", chatid, messageid, reply_markup=nav.menu
            )
            await state.set_state(ClientState.START)
        elif 'group' in call.data:
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


@dp.message_handler(state=ClientState.NEW_TASK_DATE)
async def new_task_date(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await delete_msg(message, 2)
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
        if not check_subject(message.text):
            await bot.send_message(
                chatid,
                "Такого предмета у нас нет. Вводи пожалуйста с большой буквы, например, Алгебра",
            )
            return
        await state.update_data(subject=message.text)
        if message.text == 'Английский' or message.text == "Информатика":
            markup = nav.en_group if message.text == 'Английский' else nav.info_group
            await bot.send_message(chatid, 'Какой группе это дз?', reply_markup=markup)
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
        if state_data['group'] != '':
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
        if call.data == "marks":
            await bot.edit_message_text(
                "Ждите пока мы придумаем как из циферок на бумаге сделать циферки в телефоне",
                chatid,
                messageid,
                reply_markup=nav.back_to_menu,
            )
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
            await bot.edit_message_text(
                "Ждите пока мы придумаем как сделать из нашего класса новый Китай",
                chatid,
                messageid,
                reply_markup=nav.back_to_menu,
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
                f"Добро пожаловать в меню, {db.get_user(chatid)[2]}",
                chatid,
                messageid,
                reply_markup=nav.menu,
            )
        elif call.data == "hide":
            await delete_msg(call.message, 1)
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
            day = datetime.datetime(2023, int(date.split('.')[1]), int(date.split('.')[0]))
            task_list = db.get_date_tasks(date)
            task_text = f"{weekdays[day.weekday()]} - {date}\n"
            second_name = db.get_user(chatid)[1].split()[1]
            for task in task_list:
                if task[1] == 'Английский':
                    if task[2].startswith('ОИ') and second_name in group_OI:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                    elif task[2].startswith('ИС') and not second_name in group_OI:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                elif task[1] == 'Информатика':
                    if task[2].startswith('ЕН') and second_name in group_EN:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                    elif task[2].startswith('ИВ') and not second_name in group_EN:
                        task_text += f"<i><b>{task[1]}</b></i>: {task[2][3:]}\n\n"
                else:
                    task_text += f"<i><b>{task[1]}</b></i>: {task[2]}\n\n"
            await bot.edit_message_text(
                task_text,
                chatid,
                messageid,
                reply_markup=nav.get_files_markup(task_list),
                parse_mode='HTML'
            )
    except Exception as e:
        await err(e, chatid)


@dp.message_handler(content_types=["text"], state=ClientState.all_states)
async def text(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        await bot.send_message(
            message.chat.id,
            "Ну и зачем ты мне отправил какой-то непонятный для меня текст?",
        )
    except Exception as e:
        await err(e, chatid)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
