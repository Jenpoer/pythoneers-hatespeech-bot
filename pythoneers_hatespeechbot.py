import telebot
from model_predict import predict

from preprocessing import preprocess_text

bot = telebot.TeleBot(
    "2087987681:AAG813Ais8YRNy4nlhrHZTK5UfQc4ZYa55Y", parse_mode=None)

# for /start and /help commands


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Enter a message and we'll predict if it's hateful or not.")


@bot.message_handler(commands=['preprocess'])
def send_welcome(message):
    bot.reply_to(message, preprocess_text(message.text))


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    toReturn = predict(message.text)
    if toReturn == 1:
        bot.reply_to(message, "Your message is hate")
    else:
        bot.reply_to(message, "Your message is fine")

    # not replying to the toReturn	# bot.send_message(message.chat.id, "it's working!!")


bot.infinity_polling()
