# 483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60   @telestandx_bot
import requests
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import ParseMode

from server.factory import StandFactory, QueueFactory
from server.utils.characters import AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8


class BotRoutine:
    def __init__(self, stands, proxy_url=None):
        self.stands = stands

        if proxy_url:
            self.updater = Updater(token='483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60', request_kwargs={
              'proxy_url': proxy_url,
            })
        else:
            self.updater = Updater(token='483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60')

        self.handler = CommandHandler('stands', self.stands_cmd)
        self.updater.dispatcher.add_handler(self.handler)
        self.handler = CommandHandler('1', self.alias_test, pass_args=True)
        self.updater.dispatcher.add_handler(self.handler)
        #self.install_handler('stands', self.stands_cmd)
        #self.install_handler('1', self.alias_test, pass_args=True)

    def start(self):
        self.updater.start_polling()

    def stands_cmd(self, bot, update):
        bot.send_message(
            parse_mode=ParseMode.MARKDOWN,
            chat_id=update.message.chat_id,
            text='{0} - Можно забирать \n'
                 '{2} - Занят \n'
                 '{1} - Есть активность за последние 15 минут \n'
                .format(AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8)
        )

        msg = ''
        for stand in self.stands:
            msg += '{}\n\n'.format(str(stand))

        bot.send_message(parse_mode=ParseMode.MARKDOWN, chat_id=update.message.chat_id, text=msg)

    def alias_test(self, bot, update, args):
        '''
            Examples of aliases:
                /1        - Show basic info and queue
                /1 take   - Take the stand
                /1 give   - Give the stand to person
                /1 return - Return the stand
                /take 1,2,3,4,5,6,7,8,9 - Take multiply stands
                /giveup   - Free all queue's
        '''
        bot.send_message(
            parse_mode=ParseMode.MARKDOWN,
            chat_id=update.message.chat_id,
            text='{0} *192.168.38.201 [alias /1]*\n`cl_all`\n\n'
                .format(AVAIL_SMILE_UTF8, WARNING_SMILE_UTF8, CROSS_SMILE_UTF8)
        )
        print(args)


if __name__ == '__main__':
    stands = {}
    for stand in StandFactory.get():
        stand.set_queue(QueueFactory.get_one())
        stands[str(stand)] = stand

    bot = BotRoutine(stands, proxy_url='http://127.0.0.1:3128')
    bot.start()

