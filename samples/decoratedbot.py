#!/usr/bin/env python
#-*- coding: utf8 -*-
"""A Bot to demonstrate the power of decorators
"""

from cmdbot.core import Bot
from cmdbot.decorators import direct, admin, no_verb_function
from cmdbot.configs import ArgumentConfiguration


class ArgumentBot(Bot):
    config_class = ArgumentConfiguration

    @direct
    def do_direct(self, line):
        self.say('I only say that because you summon me')

    @admin
    def do_admin(self, line):
        self.say("I only say that because you're an admin")

    @admin
    @direct
    def do_direct_admin(self, line):
        self.say("I only say that because you summon me as an admin")

    @no_verb_function
    def nothing_special(self, line):
        self.say('I say nothing special, you did not include a known verb')


if __name__ == '__main__':
    bot = ArgumentBot()
    bot.run()
