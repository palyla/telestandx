# 483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60   @telestandx_bot
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import ParseMode


AVAIL_SMILE_UTF8 = b'\xE2\x9C\x85'.decode('utf8')
CROSS_SMILE_UTF8 = b'\xE2\x9D\x8C'.decode('utf8')
WARNING_SMILE_UTF8 = b'\xE2\x9A\xA0'.decode('utf8')


def stands(bot, update):
    bot.send_message(
        parse_mode=ParseMode.MARKDOWN,
        chat_id=update.message.chat_id,
        text='{0} - Можно забирать \n'
             '{2} - Занят \n'
             '{1} - Есть активность за последние 15 минут \n'
            .format(AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8)
    )

    bot.send_message(
        parse_mode=ParseMode.MARKDOWN,
        chat_id=update.message.chat_id,
        text='{0} *192.168.38.201 [/1]*\n`cl_all`\n\n'
             '{1} *192.168.38.202 [/2]*\n`ig-10 hw-100-x1 hw-100-x2 hw-100-x3 hw-100-x8 hw-100-n1 xf-100-n1 kb-100-n1`\n\n'
             '{1} *192.168.38.203 [/3]*\n`hw-1000-q2 hw-1000-q3 hw-1000-q4 hw-2000-q2 hw-2000-q3 hw-5000-q1 xf-1000-q4 xf-5000-q1`\n\n'
             '{2} *192.168.38.204 [/4]*\n`xf-va`\n\n'
            .format(AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8)
    )


if __name__ == '__main__':
    updater = Updater(token='483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60')
    stands_handler = CommandHandler('stands', stands)
    updater.dispatcher.add_handler(stands_handler)
    updater.start_polling()

