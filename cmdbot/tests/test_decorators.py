import unittest
from cmdbot.core import Bot
from cmdbot.decorators import no_verb_function


class MockConfig(object):
    def __init__(self):
        self.host = self.chan = self.port = self.nick = ""
        self.ident = self.realname = ""
        self.admins = []


class DecoratedBot(Bot):
    config_class = MockConfig

    def undecorated(self, line):
        pass

    @no_verb_function
    def decorated(self, line):
        pass


class BrainTestCase(unittest.TestCase):

    def test_property(self):
        b = DecoratedBot()
        self.assertTrue(hasattr(b, 'no_verb_functions'))
        self.assertTrue(b.decorated in b.no_verb_functions)
