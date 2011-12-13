from cmdbot.core import Bot
from cmdbot.decorators import direct, admin

"""This bot "remembers" who spoke to it last. Example:

    22:53 -!- cmdbot [~cmdbot@127.0.0.1] has joined #cdc
    22:53 < cmdbot> Hi everyone.
    22:54 < No`> cmdbot: hello
    22:54 < cmdbot> No`: hello
    22:54 < No`> cmdbot: who
    22:54 < cmdbot> The one that talked to me last: No`
"""


class BrainyBot(Bot):

    @direct
    def do_hello(self, line):
        "Reply hello and save that in brain"
        self.say("%s: hello" % line.nick_from)
        self.brain.who_said_hello_last = line.nick_from

    @direct
    def do_who(self, line):
        "Tell us who talked to you last"
        if self.brain.knows('who_said_hello_last'):
            self.say("The one that talked to me last: %s" % self.brain.who_said_hello_last)
        else:
            self.say("Nobody has talked to me...")

    @admin
    def do_admins(self, line):
        "Tell the people who's the boss"
        self.say("My bosses: %s" % ', '.join(self.admins))

if __name__ == '__main__':
    bot = BrainyBot()
    bot.run()
