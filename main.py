import random
import os
import json
import telebot
from telebot import types
from config import telegram_token, admin_id

telegram_bot = telebot.TeleBot(telegram_token)


# Функция для сохранения переменной в JSON
def save_variable(variable, variable_name, filename='data/settings.json'):
    with open(filename, "w") as f:
        json.dump({variable_name: variable}, f)


# Функция для загрузки переменной из JSON
def load_variable(variable_name, filename='data/settings.json'):
    with open(filename, "r") as f:
        data = json.load(f)
        return data[variable_name]


# Переменные состояния
waitingFilesToUpdate_collegeLessons = set()

# Временные переменные
lessons_fileID = load_variable('lessons_fileID')
var_fileID = []

@telegram_bot.message_handler(commands=['start', 'help'])
def send_welcome_text(message):
    print(message.text, message)
    name = message.from_user.first_name

    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.row(
        types.KeyboardButton("О нас"),
        types.KeyboardButton('Дни открытых дверей'),
    )
    keyboard.row(
        telebot.types.KeyboardButton('Специальности'),
        types.KeyboardButton('Приемная комиссия'),
    )
    keyboard.row(
        types.KeyboardButton('Расписание'),
        types.KeyboardButton('Курсы')
    )
    if message.chat.id in admin_id:
        keyboard.row(types.KeyboardButton('Обновление'))

    telegram_bot.reply_to(message, f'Здравствуйте, {name}!\n'
                                   'Я помощник Юридического колледжа.\n'
                                   'Воспользуйтесь клавиатурой, чтобы отправить команду.', reply_markup=keyboard)
    return


@telegram_bot.message_handler(commands=['stop'])
def stop_pulling_bot(message):
    # print(message.chat.id, admin_id)
    if message.chat.id in admin_id:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Убить! ❌', callback_data='stopPullingBot_press'))
        telegram_bot.reply_to(message, text="Вы хотите меня убить?", parse_mode='Markdown', reply_markup=keyboard)
    return

@telegram_bot.message_handler(commands=['update'])
def update_bot(message):
    # print(message.chat.id, admin_id)
    if message.chat.id in admin_id:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Расписание занятий', callback_data='updateCollegeLessons'))
        telegram_bot.reply_to(message, text="Что Вы хотите обновить?", parse_mode='Markdown', reply_markup=keyboard)
    return


@telegram_bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(message.text, message)
    response_text = None
    keyboard = None
    photo = None

    if message.text == 'О нас': # Если сообщение 'О нас'
        # Передаем в переменную текст
        response_text = (
        "***«Познаем настолько, насколько любим»***\n\n"
        "На этом древнем мудром изречении как на фундаменте выстраиваются воспитательная и учебная работы в Юридическом колледже.\n"
        "Для наших курсантов созданы комфортные условия для получения необходимых знаний и навыков по выбранным ими специальностям. Мы осознаем, какая нелегкая задача у нашего коллектива, так как мы готовим наших курсантов не просто к работе, а к служению на благо нашего Отечества.\n"
        "Всех, кто готов поверить нам, что ваша жизнь и судьба будут нам не безразличны, приглашаем к нам учиться.\n\n"
        "    С уважением,\n"
        "директор Юридического колледжа Самойлов Георгий Владимирович"
        )
        # Создаем параметры клавиатуры
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Наши достижения', url='https://lawcol.mskobr.ru/o-nas/nashi-dostizheniya'))
        keyboard.add(types.InlineKeyboardButton(text='Сотрудничество с вузами',
                                                url='https://lawcol.mskobr.ru/o-nas/sotrudnichestvo-s-vuzami'))
        keyboard.add(types.InlineKeyboardButton(text='Вакансии и работодатели',
                                                url='https://lawcol.mskobr.ru/uchashimsya/centr-trudoustrojstva/vakansii-i-rabotodateli'))
        keyboard.add(
            types.InlineKeyboardButton(text='Общественная жизнь', callback_data='publicLife_inlineButton_press'))
        # Прикрепляем фото
        photo = open('data/images/LawColLogo_img.jpg', 'rb')

    elif message.text == 'Дни открытых дверей':
        response_text = (
            "***Приглашаем учащихся 8-10 классов на Дни открытых дверей!***\n\n"
        )
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/postuplenie-v-kolledzh/dni-otkrytyh-dverej'))

        photo = open('data/images/openDoors_img.jpg', 'rb')

    elif message.text == 'Специальности':
        response_text = (
            "Правильный выбор специальности влияет на жизнь человека, придает уверенность, обеспечивает комфорт и благополучие, определяет весь дальнейший путь, является залогом успеха и способствует построению собственной профессиональной карьеры!"
        )
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/postuplenie-v-kolledzh/specialnosti-professii'))
        links = ['specialties_img.jpg', 'specialties2_img.jpg']
        photo = open(f'data/images/{links[random.randint(0, len(links)-1)]}', 'rb')

    elif message.text == 'Приемная комиссия':
        response_text = (
            "Сотрудники приемной комиссии ответят на ваши вопросы и помогут подобрать программу обучения\n"
            "Часы приема:  \n"
            # "    ● понедельник 9.00-18.00, перерыв 13.00-13.45\n"
            "    ● вторник 9.00 – 18.00, перерыв 13.00 – 13.45\n"
            "    ● среда 9.00 – 18.00, перерыв 13.00 – 13.45\n"
            "    ● четверг 9.00 – 18.00, перерыв 13.00 – 13.45\n"
            "    ● пятница 9.00 – 16.45, перерыв 13.00 – 13.45\n\n"
            "Телефон для справок: 8 (495) 392-72-44\n"
            "Электронная почта: priem.kolleg@yandex.ru"
        )
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/postuplenie-v-kolledzh/priemnaya-komissiya'))
        photo = open('data/images/priem_img.jpg', 'rb')

    elif message.text == 'Расписание':
        # response_text = (
        #     "Более подробно с расписанием учебных занятий, внутренним распорядком дня, учебным календарем, практической подготовкой и расписанием экзаменов вы можете ознакомиться по ссылке")
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Звонки', callback_data='collegeBells'),
            types.InlineKeyboardButton(text='Занятия', callback_data='collegeLessons')
        )
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/uchashimsya/raspisanie-kanikuly')
        )
        links = ['timeTable_img.jpg', 'timeTable2_img.jpg']
        photo = open(f'data/images/{links[random.randint(0, len(links)-1)]}', 'rb')

    elif message.text == 'Курсы':
        response_text = (
            "Курсы окажут помощь учащимся в процессе выбора профиля обучения и сферы будущей профессиональной деятельности в соответствии со своими возможностями, способностями и с учетом требований рынка труда\n\n"
            "Телефон для справок: 8 (495) 392-72-44\n"
        )
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/dop-obr/kruzhki-dlya-detej/dlya-9-klassov'))

        links = ['kursi_img.jpg', 'kursi2_img.jpg', 'kursi3_img.jpg']
        photo = open(f'data/images/{links[random.randint(0, len(links)-1)]}', 'rb')

    elif message.text == 'Обновление':
        update_bot(message)
        return

    # Алгоритм отправки сообщений
    if photo:
        telegram_bot.send_photo(message.chat.id, photo, caption=response_text, parse_mode='Markdown', reply_markup=keyboard)
    elif response_text:
        telegram_bot.reply_to(message, text=response_text, parse_mode='Markdown', reply_markup=keyboard)
    return


@telegram_bot.message_handler(content_types=['document'])
def handle_documents(message):
    if message.chat.id in waitingFilesToUpdate_collegeLessons:
        file_id = message.document.file_id
        var_fileID.append(file_id)

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Готово',
                                       callback_data='doneUpdateCollegeLessons'))
        telegram_bot.send_message(message.chat.id,'Файл успешно получен!\n\nОтправьте еще, либо нажмите кнопку «Готово»', reply_markup=keyboard)
    return


@telegram_bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    print(call.data, call)
    if call.data == 'publicLife_inlineButton_press':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Волонтерское движение',
                                                url='https://lawcol.mskobr.ru/o-nas/obshchestvennaya-zhizn/volunteer-dvizhenie'))
        keyboard.add(types.InlineKeyboardButton(text='Движение первых',
                                                url='https://lawcol.mskobr.ru/proekty/vserossijskie-i-mezhdunarodnye-proekty/rossijskoe-dvizhenie-shkolnikov'))
        keyboard.add(types.InlineKeyboardButton(text='Правовая Москва',
                                                url='https://lawcol.mskobr.ru/proekty/nashi-proekty/pravovaya-moskva'))
        keyboard.add(types.InlineKeyboardButton(text='Театр в колледже',
                                                url='https://lawcol.mskobr.ru/proekty/nashi-proekty/teatr-v-kolledje'))
        keyboard.add(types.InlineKeyboardButton(text='Назад ↩️',
                                                callback_data='publicLife_inlineButton_cancel'))

        telegram_bot.answer_callback_query(callback_query_id=call.id, text='Клавиатура изменена')
        telegram_bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                               message_id=call.message.message_id,
                                               # text='Наша общественная жизнь:',
                                               reply_markup=keyboard)
        return

    elif call.data == 'publicLife_inlineButton_cancel':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Общая информация',
                                       url='https://lawcol.mskobr.ru/o-nas/obshaya-informatciya'))
        keyboard.add(types.InlineKeyboardButton(text='Педагогический состав',
                                                url='https://lawcol.mskobr.ru/o-nas/pedagogicheskii-sostav'))
        keyboard.add(
            types.InlineKeyboardButton(text='Наши достижения',
                                       url='https://lawcol.mskobr.ru/o-nas/nashi-dostizheniya'))
        keyboard.add(types.InlineKeyboardButton(text='Сотрудничество с вузами',
                                                url='https://lawcol.mskobr.ru/o-nas/sotrudnichestvo-s-vuzami'))
        keyboard.add(types.InlineKeyboardButton(text='Общественная жизнь',
                                                callback_data='publicLife_inlineButton_press'))
        telegram_bot.answer_callback_query(callback_query_id=call.id, text='Клавиатура изменена')
        telegram_bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                               message_id=call.message.message_id,
                                               # text='Наша общественная жизнь:',
                                               reply_markup=keyboard)

    elif call.data == 'collegeLessons':
        response_text = (
            "Расписание занятий:"
        )
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Звонки',
                                       callback_data='collegeBells'))
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/uchashimsya/raspisanie-kanikuly'))

        for item in lessons_fileID:
            telegram_bot.send_document(call.from_user.id, document=item)

        telegram_bot.send_message(call.from_user.id, text=response_text, parse_mode='Markdown', reply_markup=keyboard)

    elif call.data == 'collegeBells':
        response_text = (
            "Расписание звонков:"
        )
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Занятия',
                                       callback_data='collegeLessons'))
        keyboard.add(
            types.InlineKeyboardButton(text='Подробнее',
                                       url='https://lawcol.mskobr.ru/uchashimsya/raspisanie-kanikuly'))
        photo = open('data/images/collegeBells_img.jpg', 'rb')

        telegram_bot.send_photo(call.from_user.id, photo, caption=response_text, parse_mode='Markdown',
                                reply_markup=keyboard)

    elif call.data == 'updateCollegeLessons':
        if not call.from_user.id in admin_id:
            telegram_bot.send_message(call.from_user.id, 'У вас нет на это прав!')
            return

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Отмена',
                                       callback_data='doneUpdateCollegeLessons'))
        telegram_bot.send_message(call.from_user.id, 'Пришлите файлы с расписанием:', reply_markup=keyboard)
        waitingFilesToUpdate_collegeLessons.add(call.from_user.id)

    elif call.data == 'doneUpdateCollegeLessons':
        if not call.from_user.id in admin_id:
            return
        if not call.from_user.id in waitingFilesToUpdate_collegeLessons:
            return
        else:
            waitingFilesToUpdate_collegeLessons.remove(call.from_user.id)

        if not var_fileID:
            telegram_bot.send_message(call.from_user.id, 'Вы отменили обновление расписания.')
        else:
            lessons_fileID.clear()
            for item in var_fileID[:]:
                lessons_fileID.append(item)
            var_fileID.clear()
            save_variable(lessons_fileID, 'lessons_fileID')

            telegram_bot.send_message(call.from_user.id, 'Расписание обновлено!')
            print(lessons_fileID)

    elif call.data == 'stopPullingBot_press':
        telegram_bot.send_message(call.from_user.id, 'Убит наповал')
        telegram_bot.stop_polling()
        return

    return


if __name__ == '__main__':
    telegram_bot.infinity_polling()