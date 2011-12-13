"""
Config file modules. Here you can pick your favorite configuration tool to
handle bot parameters.

"""
import argparse
from ConfigParser import SafeConfigParser

# these arguments have a default value.
DEFAULT_VARS = {
    'port': '6667',
    'nick': 'cmdbot',
    'ident': 'cmdbot',
    'realname': 'Cmd Bot',
    'admins': '',
}


class GenericConfiguration(object):

    def __repr__(self):
        result = []
        keys = ('host', 'chan', 'port', 'nick')
        for key in keys:
            result.append('* %s' % getattr(self, key))
        result.append('* %s' % ', '.join(self.admins))
        return '\n'.join(result)


class IniFileConfiguration(GenericConfiguration):
    "Basic Configuration class. Loads a .ini file "
    def __init__(self):
        parser = argparse.ArgumentParser("CmdBot")
        parser.add_argument('ini_file',
            help='path to the ini file to extract configuration from')
        args = parser.parse_args()

        config = SafeConfigParser()
        config.read(args.ini_file)

        # Host and chan are the only arguments that *need* a user-defined value
        self.host = config.get('general', 'host')
        self.chan = str(config.get('general', 'chan'))

        self.port = int(config.get('general', 'port', vars=DEFAULT_VARS))
        self.nick = config.get('general', 'nick', vars=DEFAULT_VARS)
        self.ident = config.get('general', 'ident', vars=DEFAULT_VARS)
        self.realname = config.get('general', 'realname', vars=DEFAULT_VARS)
        # special case: admins
        if config.has_option("general", "admins"):
            admins = config.get('general', 'admins')
            if ',' in admins:
                admins = admins.split()
            else:
                admins = [admins]
        else:
            admins = []
        self.admins = admins


class ArgumentConfiguration(GenericConfiguration):
    "Argument-based configuration."
    def __init__(self):
        parser = argparse.ArgumentParser("CmdBot")
        # mandatory arguments
        parser.add_argument('host', help="host name")
        parser.add_argument('chan',
            help='chan name. Mind not to add the "#" as a first character')
        # optional arguments
        parser.add_argument('--port', default=DEFAULT_VARS['port'], type=int,
            help='The port number.')
        parser.add_argument('--ident', default=DEFAULT_VARS['ident'],
            help='The string to use to authenticate with the servers')
        parser.add_argument('--nick', default=DEFAULT_VARS['nick'],
            help="Your bot's nickname")
        parser.add_argument('--realname', default=DEFAULT_VARS['realname'],
            help="What will be used as a 'real name' by your bot")
        parser.add_argument('--admins', default='',
            help="A list of comma-separated nicks that will be your bot's admins")

        args = parser.parse_args()

        self.host = args.host
        self.chan = '#%s' % args.chan
        self.port = int(args.port)
        self.nick = args.nick
        self.ident = args.ident
        self.realname = args.realname
        # special case
        self.admins = args.admins.split(',')
