import telebot


access_token = '407965669:AAEiO1UUn1j6zY-QLkvevBWbNm83oEkzdok' #YOUR TOKEN
bot = telebot.TeleBot(access_token)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

