import unittest
from cmdbot.core import Bot
from cmdbot.decorators import no_verb


class MockConfig(object):
    def __init__(self):
        self.host = self.chan = self.port = self.nick = ""
        self.ident = self.realname = ""
        self.admins = []


class DecoratedBot(Bot):
    config_class = MockConfig

    def undecorated(self, line):
        "Undecorated function"
        pass

    @no_verb
    def decorated(self, line):
        "Decorated function"
        pass


class BrainTestCase(unittest.TestCase):

    def test_no_verb(self):
        b = DecoratedBot()
        self.assertTrue(hasattr(b, 'no_verb_functions'))  # the list is present
        self.assertTrue(b.decorated in b.no_verb_functions)
        self.assertFalse(b.undecorated in b.no_verb_functions)
