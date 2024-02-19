import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from telegram import Bot, Update
from telegram.ext import *
from config import telegram_token, vk_token, vk_group_id, admin_id


# Инициализация Telegram бота
telegram_bot = Bot(token=telegram_token)
updater = Updater(bot=telegram_bot, update_queue=None)

# Инициализация VK бота
vk_session = vk_api.VkApi(token=vk_token)
vk_longpoll = VkBotLongPoll(vk_session, vk_group_id)


async def message_handler_tg(update: Update, context: CallbackContext) -> None:
    print(update)
    message = update.message.text
    chat_id = update.message.chat_id
    print(chat_id, message)
    return

def message_handler_vk(event):
    print(event.type)
    if event.type == VkBotEventType.MESSAGE_NEW:
        print('Новое сообщение:')

        print('Для меня от: ', end='')

        print(event.obj.from_id)

        print('Текст:', event.object.message.text)
    return


# Запуск пула
for event in vk_longpoll.listen():
    print(event)
    message_handler_vk(event)


application = Application.builder().token(telegram_token).build()
application.add_handlr(MessageHandler(filters.ALL, message_handler_tg))
application.run_polling()