import telebot
#from preprocessing import

bot = telebot.TeleBot("2090572506:AAEJatVb5sGq1ILgNIj5cldM5UJQMQNC0y8", parse_mode=None)

## for /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)
	
	## not replying to the msg
	bot.send_message(message.chat.id, "it's working!!")

bot.infinity_polling()
