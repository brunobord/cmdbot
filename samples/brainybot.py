import argparse
from ConfigParser import SafeConfigParser
from cmdbot.core import Bot, direct

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
        if hasattr(self.brain, 'who_said_hello_last'):
            self.say("The one that talked to me last: %s" % self.brain.who_said_hello_last)
        else:
            self.say("Nobody has talked to me...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("BrainyBot")
    parser.add_argument('ini_file',
        help='path to the ini file to extract configuration from')
    args = parser.parse_args()

    config = SafeConfigParser()
    config.read(args.ini_file)
    bot = BrainyBot(config)
    bot.run()
