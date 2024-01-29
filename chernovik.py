import telebot
from telebot import types
from config import telegram_token

bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Нажми меня', callback_data='change_keyboard')
    markup.add(button)
    bot.send_message(message.chat.id, 'Привет! Нажми кнопку, чтобы изменить клавиатуру.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'change_keyboard':
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Новая кнопка', callback_data='new_button_pressed')
        keyboard.add(button)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=keyboard)
        bot.answer_callback_query(callback_query_id=call.id, text='Клавиатура изменена!')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_message(message.chat.id, 'Просто текст.')

if __name__ == "__main__":
    bot.polling(none_stop=True)
