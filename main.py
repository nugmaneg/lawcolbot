import requests
import json
import telebot
from telebot import types
from config import telegram_token

telegram_bot = telebot.TeleBot(telegram_token)


@telegram_bot.message_handler(commands=['start', 'help'])
def send_welcome_text(message):
    print(message)
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

    telegram_bot.reply_to(message, f'Здравствуйте, {name}!\n'
                                   'Я помощник Юридического колледжа.\n'
                                   'Воспользуйтесь клавиатурой, чтобы отправить команду.', reply_markup=keyboard)
    return


@telegram_bot.message_handler(func=lambda message: message.text == "О нас")
def handle_about_us(message):
    about_us_text = (
        "***«Познаем настолько, насколько любим»***\n\n"
        "На этом древнем мудром изречении как на фундаменте выстраиваются воспитательная и учебная работы в Юридическом колледже.\n"
        "Для наших курсантов созданы комфортные условия для получения необходимых знаний и навыков по выбранным ими специальностям. Мы осознаем, какая нелегкая задача у нашего коллектива, так как мы готовим наших курсантов не просто к работе, а к служению на благо нашего Отечества.\n"
        "Всех, кто готов поверить нам, что ваша жизнь и судьба будут нам не безразличны, приглашаем к нам учиться.\n\n"
        "    С уважением,\n"
        "директор Юридического колледжа Самойлов Георгий Владимирович"
    )

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Общая информация', url='https://lawcol.mskobr.ru/o-nas/obshaya-informatciya'))
    keyboard.add(types.InlineKeyboardButton(text='Педагогический состав', url='https://lawcol.mskobr.ru/o-nas/pedagogicheskii-sostav'))
    keyboard.add(types.InlineKeyboardButton(text='Наши достижения', url='https://lawcol.mskobr.ru/o-nas/nashi-dostizheniya'))
    keyboard.add(types.InlineKeyboardButton(text='Сотрудничество с вузами', url='https://lawcol.mskobr.ru/o-nas/sotrudnichestvo-s-vuzami'))
    keyboard.add(types.InlineKeyboardButton(text='Общественная жизнь', callback_data='publicLife_inlineButton_press'))

    with open('data/images/LawColLogo_img.jpg', 'rb') as photo:
        telegram_bot.send_photo(message.chat.id, photo, caption=about_us_text, parse_mode='Markdown', reply_markup=keyboard)
    return


@telegram_bot.callback_query_handler(func=lambda call: call.data == 'publicLife_inlineButton_press')
def handle_callback(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Спортивный клуб',
                                            url='https://lawcol.mskobr.ru/o-nas/obshchestvennaya-zhizn/sport-club'))
    keyboard.add(types.InlineKeyboardButton(text='Волонтерское движение',
                                            url='https://lawcol.mskobr.ru/o-nas/obshchestvennaya-zhizn/volunteer-dvizhenie'))
    keyboard.add(types.InlineKeyboardButton(text='Олимпиадное движение',
                                            url='https://lawcol.mskobr.ru/o-nas/obshchestvennaya-zhizn/olimpiadnoe-dvijenie'))
    keyboard.add(types.InlineKeyboardButton(text='Назад ↩️',
                                            callback_data='publicLife_inlineButton_cancel'))

    telegram_bot.answer_callback_query(callback_query_id=call.id, text='Клавиатура изменена')
    telegram_bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          # text='Наша общественная жизнь:',
                          reply_markup=keyboard)
    return


@telegram_bot.callback_query_handler(func=lambda call: call.data == 'publicLife_inlineButton_cancel')
def handle_callback(call):
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
    return


@telegram_bot.message_handler(func=lambda message: message.text == "Дни открытых дверей")
def handle_openDoors(message):
    response_text = (
        "***Приглашаем учащихся 8-10 классов на Дни открытых дверей!***\n\n"
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Подробнее', url='https://lawcol.mskobr.ru/postuplenie-v-kolledzh/dni-otkrytyh-dverej'))

    with open('data/images/openDoors_img.jpg', 'rb') as photo:
        telegram_bot.send_photo(message.chat.id, photo, caption=response_text, parse_mode='Markdown', reply_markup=keyboard)
    return


@telegram_bot.message_handler(func=lambda message: message.text == "Специальности")
def handle_specializations(message):
    response_text = (
        "Правильный выбор специальности влияет на жизнь человека, придает уверенность, обеспечивает комфорт и благополучие, определяет весь дальнейший путь, является залогом успеха и способствует построению собственной профессиональной карьеры!"
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Подробнее', url='https://lawcol.mskobr.ru/postuplenie-v-kolledzh/specialnosti-professii'))

    telegram_bot.reply_to(message, response_text, parse_mode='Markdown', reply_markup=keyboard)

    return


@telegram_bot.message_handler(func=lambda message: message.text == "Приемная комиссия")
def handle_admissionCommittee(message):
    response_text = (
        "***Приходите! Мы Вас ждем!!!***\n\n"
        "Сотрудники приемной комиссии ответят на ваши вопросы и помогут подобрать программу обучения\n"
        "Телефон для справок: 8 (495) 392-72-44\n"
        "Часы приема:  \n"
        "    ● понедельник 9.00-18.00, перерыв 13.00-13.45\n"
        "    ● вторник 9.00 – 18.00, перерыв 13.00 – 13.45\n"
        "    ● среда 9.00 – 18.00, перерыв 13.00 – 13.45\n"
        "    ● четверг 9.00 – 18.00, перерыв 13.00 – 13.45\n"
        "    ● пятница 9.00 – 16.45, перерыв 13.00 – 13.45\n\n"
        "Электронная почта: priem.kolleg@yandex.ru"
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Подробнее', url='https://lawcol.mskobr.ru/postuplenie-v-kolledzh/specialnosti-professii'))

    telegram_bot.reply_to(message, response_text, parse_mode='Markdown', reply_markup=keyboard)

    return


@telegram_bot.message_handler(func=lambda message: message.text == "Расписание")
def handle_openDoors(message):
    response_text = (
        "Более подробно с расписанием учебных занятий, внутренним распорядком дня, учебным календарем, практической подготовкой и расписанием экзаменов вы можете ознакомиться по ссылке"
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Подробнее', url='https://lawcol.mskobr.ru/uchashimsya/raspisanie-kanikuly'))

    with open('data/images/timetable_img.jpg', 'rb') as photo:
        telegram_bot.send_photo(message.chat.id, photo, caption=response_text, parse_mode='Markdown', reply_markup=keyboard)
    return


@telegram_bot.message_handler(func=lambda message: message.text == "Курсы")
def handle_admissionCommittee(message):
    response_text = (
        "Курсы окажут помощь учащимся в процессе выбора профиля обучения и сферы будущей профессиональной деятельности в соответствии со своими возможностями, способностями и с учетом требований рынка труда\n\n"
        "*** Для зачисления на обучение Вам необходимо: ***\n"
        "    ● перейти на портал государственных услуг города Москвы по ссылке pgu.mos.ru;\n"
        "    ● выбрать «Запись в кружки, спортивные секции, дома творчества»;\n"
        "    ● пройти процедуру записи.\n"
        "Более подробную информацию вы можете получить пройдя по ссылке\n\n"
        "Телефон для справок: 8 (495) 392-72-44\n"
    )
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='Подробнее', url='https://lawcol.mskobr.ru/dop-obr/kruzhki-dlya-detej/dlya-9-klassov'))

    with open('data/images/kursi_img.png', 'rb') as photo:
        telegram_bot.send_photo(message.chat.id, photo, caption=response_text, parse_mode='Markdown', reply_markup=keyboard)
    return


if __name__ == '__main__':
    telegram_bot.polling(non_stop=True)