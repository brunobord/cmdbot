#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""Cmd Bot, a bot with a brainy cmd attitude.

This is the core bot module. It's already usable, even if you can't actually
use it for something interesting.

Every other bot you will want to build with this module can be class that
extends the Bot main class.
"""
import os
import sys
import socket
import logging
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('cmdbot')
logger.addHandler(console)

#i18n installation
import gettext
try:
    locale_path = os.path.join(os.path.dirname(os.path.abspath('.')), 'locale')
    t = gettext.translation('cmdbot', locale_path)
    t.install()
    _ = t.gettext
except:
    _ = gettext.gettext
    logger.info(u'Translation Not Found. Fallback to default')

from cmdbot.configs import IniFileConfiguration
from cmdbot.decorators import direct


class Line(object):
    "IRC line"
    def __init__(self, nick, message, direct=False):
        self.nick_from = nick
        self._raw_message = message
        self.message = message.lower()
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

    welcome_message = _('Hi everyone.')
    exit_message = _('Bye, all')
    # One can override this
    config_class = IniFileConfiguration
    aliases = {}

    def __init__(self):
        self.config = self.config_class()
        # special case: admins
        self.admins = self.config.admins
        self.brain = self.Brain()  # this brain can contain *anything* you want.

        self.available_functions = []
        self.no_verb_functions = []
        self.no_help_functions = []
        for name in dir(self):
            func = getattr(self, name)
            if callable(func):
                if name.startswith('do_'):
                    self.available_functions.append(name.replace('do_', ''))
                    if hasattr(func, 'aliases'):
                        for alias in func.aliases:
                            self.aliases['%s' % alias] = func
                if hasattr(func, 'no_verb'):
                    self.no_verb_functions.append(func)
                if hasattr(func, "no_help"):
                    self.no_help_functions.append(func)
                    # little trick. helps finding out if function is decorated
                    self.no_help_functions.append(name.replace('do_', ''))
        logger.debug(self.no_help_functions)
        self.s = socket.socket()

    def connect(self):
        "Connect to the server and join the chan"
        logger.info(_('Connection to host...'))
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

    def reply(self, message, line=None, nick=None):
        """Reply to the initial sender. Extracts the sender from line, if
        not set in the arguments
        """
        if nick:
            self.say("%s: %s" % (nick, message))
        elif line:
            self.say("%s: %s" % (line.nick_from, message))
        else:
            logger.info("Reply message used without line or nick. Please correct")
            self.say(message)

    def me(self, message):
        "/me message"
        self.say("\x01%s %s\x01" % ("ACTION", message))

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

    def process_noverb(self, line):
        """Process the no-verb lines
        (i.e. a line with a first verb unreferenced in the do_<verb> methods."""
        for func in self.no_verb_functions:
            func(line)

    def process_line(self, line):
        "Process the Line object"
        try:
            func = None
            if line.verb.encode('utf') in self.aliases.keys():
                return self.aliases[line.verb.encode('utf')](line)
            try:
                func = getattr(self, 'do_%s' % line.verb)
            except UnicodeEncodeError:
                pass  # Do nothing, it won't work.
            except AttributeError:
                if line.direct:
                    # it's an instruction, we didn't get it.
                    self.say(_("%(nick)s: I have no clue...") % {'nick': line.nick_from})
                self.process_noverb(line)
            if func:
                return func(line)
        except:
            logger.exception('Bot Error')
            self.me("is going to die :( an exception occurred")

    def _raw_ping(self, line):
        "Raw PING/PONG game. Prevent your bot from being disconnected by server"
        self.s.send(line.replace('PING', 'PONG'))

    @direct
    def do_ping(self, line):
        "(direct) Reply 'pong'"
        self.say(_("%(nick)s: pong") % {'nick': line.nick_from})

    @direct
    def do_help(self, line):
        "(direct) Gives some help"
        self.say(_("%(nick)s: you need some help? Here is some...")
            % {'nick': line.nick_from})

        splitted = line.message.split()
        if len(splitted) == 1:
            self.say(_('Available commands: %(commands)s')
                % {'commands': ', '.join(func for func in self.available_functions if func not in self.no_help_functions)})
            if self.aliases:
                self.say(_('Available aliases: %s') % ', '.join(self.aliases.keys()))
        else:
            command_name = splitted[1]
            try:
                func = getattr(self, 'do_%s' % command_name)
                if func in self.no_help_functions:
                    raise AttributeError
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
                        logger.debug(raw_line)
                        line = self.parse_line(raw_line)
                        self.process_line(line)
        except KeyboardInterrupt:
            self.s.send('QUIT :%s\r\n' % self.exit_message)
            sys.exit(_("Bot has been shut down. See you."))
        except UnicodeEncodeError:
            logger.error('Decode error in buffer reading. Move along')


if __name__ == '__main__':
    bot = Bot()
    bot.run()
