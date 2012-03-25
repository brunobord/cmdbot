#!/usr/bin/env python
#-*- coding: utf8 -*-
"""A dummy Bot only there to illustrate how to use an ArgumentConfiguration
rather than the default IniFileConfiguration class.

If you want to run it::

    python argbot.py name.my.server mychannel

Or, if you want to customize your arguments::

    python argbot.py name.my.server mychannel --nick=specialbot --admins=me,myself

"""
from cmdbot.core import Bot
from cmdbot.decorators import direct, admin
from cmdbot.configs import ArgumentConfiguration


class ArgumentBot(Bot):
    config_class = ArgumentConfiguration

    @direct
    @admin
    def do_hello(self, line):
        self.say("You're my master")


if __name__ == '__main__':
    bot = ArgumentBot()
    bot.run()
