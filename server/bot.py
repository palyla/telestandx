# 483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60   @telestandx_bot
from telegram.ext import CommandHandler
from telegram.ext import Updater


def stands(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


updater = Updater(token='483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60')
stands_handler = CommandHandler('stands', stands)
updater.dispatcher.add_handler(stands_handler)


updater.start_polling()

