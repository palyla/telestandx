# 483769578:AAGFIRimDTitSlIXbGasW2BQX2qDrnblq60   @telestandx_bot
from functools import wraps

import logging
import requests
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import ParseMode

from server.factory import StandFactory, QueueFactory
from server.utils.characters import Emoji
from server.utils.helper import print_exceptions


LIST_OF_ADMINS = ()


def restricted(func):
    print('restricted!')

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


class SSHClientsMessage:
    def __init__(self, clients_dict):
        pass

class QueueMessage:
    def __init__(self, queue_dict):
        pass

class StateMessage:
    def __init__(self, state_dict):
        pass


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

        # self.handler = CommandHandler('test', self.alias_test, pass_args=True)
        # self.updater.dispatcher.add_handler(self.handler)

        for id, stand in self.stands.items():
            self.handler = CommandHandler(stand.alias, self.one_stand_cmd, pass_args=True)
            self.updater.dispatcher.add_handler(self.handler)

    def start(self):
        self.updater.start_polling()

    @print_exceptions
    def one_stand_cmd(self, bot, update, args):

        def print_stand_info(alias):
            stand = self.stands[alias]
            bot.send_message(
                parse_mode=ParseMode.MARKDOWN,
                chat_id=update.message.chat_id,
                text=repr(stand)
            )

        if not args:
            alias = update.message['text'][1:]
            print_stand_info(alias)

        elif 'take' in args[0]:
            alias = update.message['text'][1:].split()[0]
            stand = self.stands[alias]
            stand.new_user(update.effective_user['username'])
            print_stand_info(alias)

        elif 'return' in args[0]:
            alias = update.message['text'][1:].split()[0]
            stand = self.stands[alias]
            stand.del_user(update.effective_user['username'])
            print_stand_info(alias)

    #@restricted
    @print_exceptions
    def stands_cmd(self, bot, update):
        bot.send_message(
            parse_mode=ParseMode.MARKDOWN,
            chat_id=update.message.chat_id,
            text='`{0} - Можно забирать \n'
                 '{2} - Занят \n'
                 '{1} - Есть активность за последние 15 минут \n'
                 '{3} - Недоступен в сети \n`'
                .format(Emoji.UTF8.CHECK_MARK, Emoji.UTF8.WARNING, Emoji.UTF8.CROSS, Emoji.UTF8.SLEEP)
        )

        msg = ''
        for id, stand in self.stands.items():
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
            text='{2} *192.168.38.201* at @palyla, last activity 16:34\n'
                 'Queue: \n'
                 '1. @palyla, expecting 4 hours already\n'
                 '2. @palyla, expecting 1 hours already\n'
                 '3. @palyla, expecting less 1 hour already\n\n'
                 '{3} TEST IN PROGRESS {3}\n'
                 '`Started at 21:00\n'
                 'Current scenario modbus.xml`\n\n'
                 'SSH sessions:\n'
                 '`autotest pts/5 16:33 (10.0.112.36)\n'
                 'autotest pts/2 13:42 (192.168.38.6)`'
                .format(Emoji.UTF8.CHECK_MARK, Emoji.UTF8.WARNING, Emoji.UTF8.CROSS, Emoji.UTF8.GEAR)
        )
        print(args)


if __name__ == '__main__':
    # https://stackoverflow.com/questions/25823905/how-to-iterate-over-a-priority-queue-in-python

    stands = {}
    for stand in StandFactory.get():
        stand.set_queue(QueueFactory.get_one())
        stands[stand.alias] = stand

    bot = BotRoutine(stands, proxy_url='http://127.0.0.1:3128')
    # bot = BotRoutine(stands)
    bot.start()

