#!/usr/bin/env python
#-*- coding: utf -*-
"""Cmd Bot, a bot with a brainy cmd attitude.

This is the core bot module. It's already usable, even if you can't actually
use it for something interesting.

Every other bot you will want to build with this module can be class that
extends the Bot main class.
"""
import sys
import argparse
from ConfigParser import SafeConfigParser
from functools import wraps
import socket
import logging
logging.basicConfig(level=logging.INFO)


# Decorators
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


class Configuration(object):
    "Basic Configuration class. Loads a .ini file "
    def __init__(self):
        # the only mandatory arguments
        default_vars = {
            'port': '6667',
            'nick': 'cmdbot',
            'ident': 'cmdbot',
            'realname': 'Cmd Bot',
            'admins': '',
        }
        parser = argparse.ArgumentParser("CmdBot")
        parser.add_argument('ini_file',
            help='path to the ini file to extract configuration from')
        args = parser.parse_args()

        config = SafeConfigParser()
        config.read(args.ini_file)

        self.host = config.get('general', 'host')
        self.chan = str(config.get('general', 'chan'))

        self.port = int(config.get('general', 'port', vars=default_vars))
        self.nick = config.get('general', 'nick', vars=default_vars)
        self.ident = config.get('general', 'ident', vars=default_vars)
        self.realname = config.get('general', 'realname', vars=default_vars)
        self.admins = config.get('general', 'admins', vars=default_vars).split()


class Bot(object):
    "Main bot class"

    class Brain(object):
        pass

    welcome_message = "Hi everyone."
    exit_message = "Bye, all"
    # One can override this
    config_class = Configuration

    def __init__(self):
        self.config = self.config_class()
        # special case: admins
        self.admins = self.config.admins
        self.brain = self.Brain()  # this brain can contain *anything* you want.

        self.available_functions = []
        for name in dir(self):
            if name.startswith('do_'):
                func = getattr(self, name)
                if callable(func):
                    self.available_functions.append(name.replace('do_', ''))

        self.s = socket.socket()

    def connect(self):
        "Connect to the server and join the chan"
        logging.info("Connection to host...")
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
                self.say("%s: I have no clue..." % line.nick_from)
        if func:
            return func(line)

    def _raw_ping(self, line):
        "Raw PING/PONG game. Prevent your bot from being disconnected by server"
        logging.debug(line)
        self.s.send(line.replace('PING', 'PONG'))

    @direct
    def do_ping(self, line):
        "(direct) Reply 'pong'"
        self.say("%s: pong" % line.nick_from)

    @direct
    def do_help(self, line):
        "(direct) Gives some help"
        self.say('%s: you need some help? Here is some...' % line.nick_from)

        splitted = line.message.split()
        if len(splitted) == 1:
            self.say('Available commands: %s' % ', '.join(self.available_functions))
        else:
            command_name = splitted[1]
            try:
                func = getattr(self, 'do_%s' % command_name)
                self.say('%s: %s' % (command_name, func.__doc__))
            except AttributeError:
                self.say('Sorry, command "%s" unknown' % command_name)

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
            self.s.send('QUIT :%s' % self.exit_message)
            sys.exit("Bot has been shut down. See you.")


if __name__ == '__main__':
    bot = Bot()
    bot.run()
