#-*- coding: utf8 -*-
from functools import wraps


def direct(func):
    "Decorator: only process the line if it's a direct message"
    @wraps(func)
    def newfunc(bot, line):
        if line.direct:
            return func(bot, line)
    return newfunc


def admin(func):
    "Decorator, only process the line if the author is in the admin list"
    @wraps(func)
    def newfunc(bot, line):
        if line.nick_from in bot.config.admins:
            return func(bot, line)
    return newfunc


def contains(string):
    "Decorator, only process the line if the author mentionning the designated string"
    def real_decorator(func):
        @wraps(func)
        def newfunc(bot, line):
            if string in line.message:
                return func(bot, line)
        return newfunc
    return real_decorator


def no_verb(func):
    """Decorator: define a function that will be executed if no verb is found
    in the line"""
    func.no_verb = True
    return func
