'''
The telestandx is a Telegram bot for optimize team work with hardware stands running by Linux.
Copyright (C) 2017  Sedlyarskiy Alexey

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import os
import signal
import threading
import time
import datetime
import pickle
from functools import wraps
from collections import OrderedDict

from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import ParseMode

from server.factory import StandFactory, QueueFactory
from server.models.message import StandShortInfoMessage
from server.utils.characters import Emoji
from server.utils.helper import print_exceptions

CONNECT_TIMEOUT = 10
READ_TIMEOUT = 10

SERIALIZE_FILE = 'queues.dat'
LIST_OF_ADMINS = ()


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


class BotRoutine:
    def __init__(self, stands, proxy_url=None):
        self.stands = stands

        if proxy_url:
            self.updater = Updater(token='', request_kwargs={
                'proxy_url': proxy_url,
                'read_timeout': READ_TIMEOUT,
                'connect_timeout': CONNECT_TIMEOUT
            })
        else:
            self.updater = Updater(token='', request_kwargs={
                'read_timeout': READ_TIMEOUT,
                'connect_timeout': CONNECT_TIMEOUT
            })

        self.handler = CommandHandler('stands', self.stands_cmd)
        self.updater.dispatcher.add_handler(self.handler)

        self.handler = CommandHandler('take', self.take_cmd, pass_args=True)
        self.updater.dispatcher.add_handler(self.handler)

        self.handler = CommandHandler('free', self.free_cmd, pass_args=True)
        self.updater.dispatcher.add_handler(self.handler)

        self.handler = CommandHandler('give', self.give_cmd, pass_args=True)
        self.updater.dispatcher.add_handler(self.handler)

        self.handler = CommandHandler('giveup', self.giveup_cmd)
        self.updater.dispatcher.add_handler(self.handler)

        self.handler = CommandHandler('my', self.my_cmd)
        self.updater.dispatcher.add_handler(self.handler)

        # self.handler = CommandHandler('test', self.alias_test, pass_args=True)
        # self.updater.dispatcher.add_handler(self.handler)

        for id, stand in self.stands.items():
            self.handler = CommandHandler(stand.alias, self.one_stand_cmd, pass_args=True)
            self.updater.dispatcher.add_handler(self.handler)

    def start(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def get_stand_by_alias(self, alias):
        try:
            return self.stands[alias]
        except KeyError:
            try:
                return self.stands[alias.replace('@telestandx_bot', '')]
            except:
                return self.stands[alias.replace('@telestandx_test_bot', '')]

    def print_stand_info(self, bot, update, alias):
        stand = self.get_stand_by_alias(alias)
        chat_id = update.message.chat.id

        count = 0
        msg = repr(stand)
        for id in stand.queue:
            count += 1
            username = '{}'.format(bot.get_chat_member(chat_id, id).user.first_name)
            msg = msg.replace(str(id), username)

        bot.send_message(
            parse_mode=ParseMode.MARKDOWN,
            chat_id=update.message.chat_id,
            text=msg
        )

    @print_exceptions
    def one_stand_cmd(self, bot, update, args):
        ''' {'id': 152149972, 'first_name': 'Alexey', 'is_bot': False, 'last_name': 'Sedlyarsky', 'username': 'palyla',
         'language_code': 'en-US'} '''

        if not args:
            alias = update.message['text'][1:]
            self.print_stand_info(bot, update, alias)

        elif 'take' in args[0]:
            alias = update.message['text'][1:].split()[0]
            stand = self.get_stand_by_alias(alias)
            stand.new_user(update.effective_user['id'])
            self.print_stand_info(bot, update, alias)

        elif 'free' in args[0]:
            chat_id = update.message.chat.id
            alias = update.message['text'][1:].split()[0]
            stand = self.get_stand_by_alias(alias)
            previous_user = stand.user
            stand.del_user(update.effective_user['id'])
            self.print_stand_info(bot, update, alias)

            if stand.user != previous_user and stand.user != None:
                msg = "{}, {} is yours!".format(bot.get_chat_member(chat_id, stand.user).user.name, '/{}'.format(stand.alias))
                bot.send_message(chat_id=update.message.chat_id, text=msg)

        elif 'give' in args[0]:
            alias = update.message['text'][1:].split()[0]
            stand = self.get_stand_by_alias(alias)

            count = 0
            users_order = dict()
            for id in stand.queue:
                count += 1
                users_order[count] = id

            if len(args) >= 1:
                to_user_id = users_order[int(args[1])]

                if to_user_id != update.effective_user['id']:
                    stand.del_user(update.effective_user['id'])
                    stand.del_user(to_user_id)
                    stand.queue.queue.appendleft(to_user_id)

            self.print_stand_info(bot, update, alias)

    #@restricted
    @print_exceptions
    def stands_cmd(self, bot, update):
        chat_id = update.message.chat.id

        # bot.send_message(
        #     parse_mode=ParseMode.MARKDOWN,
        #     chat_id=update.message.chat_id,
        #     text='`{0} - Можно забирать \n'
        #          '{2} - Занят \n'
        #          '{1} - Есть активность за последние 15 минут \n'
        #          '{3} - Недоступен в сети \n`'
        #         .format(Emoji.UTF8.CHECK_MARK, Emoji.UTF8.WARNING, Emoji.UTF8.CROSS, Emoji.UTF8.SLEEP)
        # )

        msg = ''
        for id, stand in self.stands.items():
            one_stand_msg = '{}\n\n'.format(str(stand))
            if not stand.queue.empty():
                username = '@{}'.format(bot.get_chat_member(chat_id, stand.user).user.first_name)
                one_stand_msg = one_stand_msg.replace(str(stand.user), username)
            msg += one_stand_msg

        bot.send_message(parse_mode=ParseMode.MARKDOWN, chat_id=update.message.chat_id, text=msg)

    @print_exceptions
    def take_cmd(self, bot, update, args):
        aliases = update.message['text'][1:].split()[1:]
        for alias in aliases:
            stand = self.get_stand_by_alias(alias)
            stand.new_user(update.effective_user['id'])
            self.print_stand_info(bot, update, alias)

    @print_exceptions
    def free_cmd(self, bot, update, args):
        chat_id = update.message.chat.id
        aliases = update.message['text'][1:].split()[1:]
        for alias in aliases:
            stand = self.get_stand_by_alias(alias)
            previous_user = stand.user
            stand.del_user(update.effective_user['id'])
            self.print_stand_info(bot, update, alias)

            if stand.user != previous_user and stand.user != None:
                msg = "{}, {} is yours!".format(bot.get_chat_member(chat_id, stand.user).user.name, '/{}'.format(stand.alias))
                bot.send_message(chat_id=update.message.chat_id, text=msg)

    @print_exceptions
    def giveup_cmd(self, bot, update):
        for alias, stand in self.stands.items():
            try:
                previous_user = stand.user
                stand.del_user(update.effective_user['id'])
                chat_id = update.message.chat.id

                count = 0
                msg = StandShortInfoMessage(stand).message()
                for id in stand.queue:
                    count += 1
                    username = '{}'.format(bot.get_chat_member(chat_id, id).user.first_name)
                    msg = msg.replace(str(id), username)

                bot.send_message(
                    parse_mode=ParseMode.MARKDOWN,
                    chat_id=update.message.chat_id,
                    text=msg
                )
                if stand.user != previous_user and stand.user != None:
                    msg = "{}, {} is yours!".format(bot.get_chat_member(chat_id, stand.user).user.name,
                                                    '/{}'.format(stand.alias))
                    bot.send_message(chat_id=update.message.chat_id, text=msg)
            except:
                pass

    @print_exceptions
    def give_cmd(self, bot, update, args):
        alias = update.message['text'][1:].split()[1]
        stand = self.get_stand_by_alias(alias)

        count = 0
        users_order = dict()
        for id in stand.queue:
            count += 1
            users_order[count] = id

        if len(args) >= 2:
            to_user_id = users_order[int(args[1])]
            if to_user_id != update.effective_user['id']:
                stand.del_user(update.effective_user['id'])
                stand.del_user(to_user_id)
                stand.queue.queue.appendleft(to_user_id)

        self.print_stand_info(bot, update, alias)

    @print_exceptions
    def my_cmd(self, bot, update):
        for alias, stand in self.stands.items():
            if update.effective_user['id'] in stand.queue.queue:
                chat_id = update.message.chat.id
                count = 0
                msg = StandShortInfoMessage(stand).message()
                for id in stand.queue:
                    count += 1
                    username = '{}'.format(bot.get_chat_member(chat_id, id).user.first_name)
                    msg = msg.replace(str(id), username)

                bot.send_message(
                    parse_mode=ParseMode.MARKDOWN,
                    chat_id=update.message.chat_id,
                    text=msg
                )

    def alias_test(self, bot, update, args):
        '''
            Examples of aliases:
                /1          - Show basic info and queue
                /1 take     - Take the stand
                /1 give 2   - Give the stand to person, 2 is a number of queue
                /1 return   - Return the stand
                /take 1,2,3,4,5,6,7,8,9 - Take multiply stands
                /giveup     - Free all queue's
                /give 1 2   - Give the stand to person, 1 is a number of stand, 2 is a number of queue
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
    stands = OrderedDict()
    if not os.path.exists(SERIALIZE_FILE):
        for stand in StandFactory.get():
            stand.set_queue(QueueFactory.get_one())
            stands[stand.alias] = stand
    else:
        to_load = dict()
        with open(SERIALIZE_FILE, 'rb') as fd:
            try:
                to_load = pickle.load(fd)
            except:
                print('Failed to load saved queues!')

        for stand in StandFactory.get():
            for saved_alias, saved_queue in to_load.items():
                if stand.alias == saved_alias:
                    stand.queue.queue = pickle.loads(saved_queue)
            stands[stand.alias] = stand

    is_terminate = threading.Event()
    def stands_monitor():
        free_time = datetime.time(0, 0, 0)

        while True:
            if is_terminate.is_set():
                break
            now = datetime.datetime.now().time()

            for alias, stand in stands.items():
                state = stand.state
                if now == free_time and not stand.queue.empty():
                    stand.set_queue(QueueFactory.get_one())
            time.sleep(3)

    mthread = threading.Thread(target=stands_monitor, args=())
    mthread.daemon = True
    mthread.start()

    bot = BotRoutine(stands, proxy_url='http://127.0.0.1:3128')
    # bot = BotRoutine(stands)

    def handler(*args, **kwargs):
        is_terminate.set()
        mthread.join()

        bot.stop()

        to_save = dict()
        for alias, stand in stands.items():
            to_save[alias] = pickle.dumps(stand.queue.queue)
        with open(SERIALIZE_FILE, 'wb') as fd:
            pickle.dump(to_save, fd)

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    import atexit
    atexit.register(handler)

    bot.start()

