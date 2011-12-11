#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""Cmd Bot, a bot with a brainy cmd attitude.

This is the core bot module. It's already usable, even if you can't actually
use it for something interesting.

Every other bot you will want to build with this module can be class that
extends the Bot main class.
"""
import sys
from functools import wraps
import socket
import logging
logging.basicConfig(level=logging.INFO)
#i18n installation
import gettext
gettext.install('cmdbot', 'locale')
_ = gettext.gettext

from cmdbot.configs import IniFileConfiguration


def direct(func):
    "Decorator: only process the line if it's a direct message"
    @wraps(func)
    def newfunc(bot, *args, **kwargs):
        line = args[0]
        if line.direct:
            return func(bot, *args, **kwargs)
    return newfunc


def admin(func):
    "Decorator, only process the line if the author is in the admin list"
    @wraps(func)
    def newfunc(bot, *args, **kwargs):
        line = args[0]
        if line.nick_from in bot.admins:
            return func(bot, *args, **kwargs)
    return newfunc


def contains(string):
    "Decorator, only process the line if the author mentionning the designated string"
    def real_decorator(func):
        @wraps(func)
        def newfunc(bot, *args, **kwargs):
            line = args[0]
            if string in line.message:
                return func(bot, *args, **kwargs)
        return newfunc
    return real_decorator


class Line(object):
    "IRC line"
    def __init__(self, nick, message, direct=False):
        self.nick_from = str(nick)
        self.message = str(message.lower())
        self.verb = ''
        if self.message:
            self.verb = self.message.split()[0]
        self.direct = direct

    def __repr__(self):
        return '<%s: %s>' % (self.nick_from, self.message)


class Bot(object):
    "Main bot class"

    class Brain(object):

        def knows(self, key, include_falses=False):
            """Return True if the brain.key value is known *and* not None.
            If the "with_none" option is set to True, event the 'false' values
            (None, '', (), [], etc.) values are counted.
            """
            return hasattr(self, key) and (getattr(self, key) or include_falses)

    welcome_message = _("Hi everyone.")
    exit_message = _("Bye, all")
    # One can override this
    config_class = IniFileConfiguration

    def __init__(self):
        self.config = self.config_class()
        # special case: admins
        self.admins = self.config.admins
        self.brain = self.Brain()  # this brain can contain *anything* you want.

        self.available_functions = []
        for name in dir(self):
            func = getattr(self, name)
            if callable(func) and name.startswith('do_'):
                self.available_functions.append(name.replace('do_', ''))

        self.s = socket.socket()

    def connect(self):
        "Connect to the server and join the chan"
        logging.info(_("Connection to host..."))
        self.s.connect((self.config.host, self.config.port))
        self.s.send("NICK %s\r\n" % self.config.nick)
        self.s.send("USER %s %s bla :%s\r\n" % (
            self.config.ident, self.config.host, self.config.realname))
        self.s.send("JOIN :%s\r\n" % self.config.chan)
        self.say(self.welcome_message)

    def say(self, message):
        "Say that `message` to the channel"
        msg = 'PRIVMSG %s :%s\r\n' % (self.config.chan, message)
        self.s.send(msg)

    def parse_line(self, line):
        "Analyse the line. Return a Line object"
        message = nick_from = ''
        direct = False
        meta, _, raw_message = line.partition(self.config.chan)
        # strip strings
        raw_message = raw_message.strip()
        # extract initial nick
        meta = meta.strip()
        nick_from = meta.partition('!')[0].replace(':', '')

        if raw_message.startswith(':%s' % self.config.nick):
            direct = True
            _, _, message = raw_message.partition(' ')
        else:
            message = raw_message.replace(':', '').strip()
        # actually return the Line object
        return Line(nick_from, message, direct)

    def process_line(self, line):
        "Process the Line object"
        func = None
        try:
            func = getattr(self, 'do_' + line.verb)
        except AttributeError:
            if line.direct:
                # it's an instruction, we didn't get it.
                self.say(_("%(nick)s: I have no clue...") % {'nick': line.nick_from})
        if func:
            return func(line)

    def _raw_ping(self, line):
        "Raw PING/PONG game. Prevent your bot from being disconnected by server"
        logging.debug(line)
        self.s.send(line.replace('PING', 'PONG'))

    @direct
    def do_ping(self, line):
        "(direct) Reply 'pong'"
        self.say(_("%(nick)s: pong") % {'nick': line.nick_from})

    @direct
    def do_help(self, line):
        "(direct) Gives some help"
        self.say(_('%(nick)s: you need some help? Here is some...')
            % {'nick': line.nick_from})

        splitted = line.message.split()
        if len(splitted) == 1:
            self.say(_('Available commands: %(commands)s')
                % {'commands': ', '.join(self.available_functions)})
        else:
            command_name = splitted[1]
            try:
                func = getattr(self, 'do_%s' % command_name)
                self.say('%s: %s' % (command_name, func.__doc__))
            except AttributeError:
                self.say(_('Sorry, command "%(command)s" unknown')
                    % {'command': command_name})

    def run(self):
        "Main programme. Connect to server and start listening"
        self.connect()
        readbuffer = ''
        try:
            while 1:
                readbuffer = readbuffer + self.s.recv(1024).decode('utf')
                temp = readbuffer.split("\n")  # string.split
                readbuffer = temp.pop()
                for raw_line in temp:
                    raw_line = raw_line.rstrip()
                    if raw_line.startswith('PING'):
                        self._raw_ping(raw_line)
                    elif self.config.chan in raw_line and 'PRIVMSG' in raw_line:
                        logging.debug(raw_line)
                        line = self.parse_line(raw_line)
                        self.process_line(line)
        except KeyboardInterrupt:
            self.s.send('QUIT :%s\r\n' % self.exit_message)
            sys.exit(_("Bot has been shut down. See you."))


if __name__ == '__main__':
    bot = Bot()
    bot.run()
