""" my first telegram bot
t.me/Verminoid_bot """


import telebot
TOKEN = '2080700790:AAF8FyC6QlHC9Kc747AD0N00VqxymJNSbCY'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler()
def message_handler(message):
    """ echo"""
    print(message.text)

bot.infinity_polling()
