#!/usr/bin/env python
#-*- coding: utf8 -*-
"""This bot "plays" dices with you. This illustrates how to build
new decorators for actions and how to use them.
"""
import random
from functools import wraps
from cmdbot.core import Bot, direct, logging


def in_game(func):
    "Decorator: only process the line game has been started with the player"
    @wraps(func)
    def newfunc(bot, line):
        if bot.brain.knows('games') and line.nick_from in bot.brain.games:
            return func(bot, line)
        else:
            bot.say("Erm. Looks like we didn't start playing.")
    return newfunc


def diceroll():
    return random.randint(1, 6)


class GameBot(Bot):
    welcome_message = "Hi everyone. Say 'play' to me, and you'll have 3 turns."

    @direct
    def do_play(self, line):
        "Start playing with the bot"
        # initialize the game
        if not self.brain.knows('games'):
            self.brain.games = {}
        self.brain.games[line.nick_from] = {
            'turns': 0,
            'bot_score': 0,
            'player_score': 0
        }
        self.say(u'%s: So you wanna play dices?... Say "roll" and we are going to start' % line.nick_from)

    @in_game
    def do_roll(self, line):
        "Roll the dice"
        player_diceroll = diceroll()
        bot_diceroll = diceroll()
        self.say('I have made a %d and you have made a %d' % (bot_diceroll, player_diceroll))
        self.brain.games[line.nick_from]['turns'] += 1
        self.brain.games[line.nick_from]['bot_score'] += bot_diceroll
        self.brain.games[line.nick_from]['player_score'] += player_diceroll
        bot_score = self.brain.games[line.nick_from]['bot_score']
        player_score = self.brain.games[line.nick_from]['player_score']
        if self.brain.games[line.nick_from]['turns'] > 2:
            if bot_score > player_score:
                result = "I have won!"
            elif bot_score < player_score:
                result = "Congrats! You've won!"
            else:
                result = "Well... we're even."
            self.say('%s: Game over. %s (%d/%d)' % (line.nick_from, result, bot_score, player_score))
            del self.brain.games[line.nick_from]
        scores = "Scores: Bot %d - %d %s" % (bot_score, player_score, line.nick_from)
        logging.info(scores)
        self.say(scores)


if __name__ == '__main__':
    bot = GameBot()
    bot.run()
