"""
Config file modules. Here you can pick your favorite configuration tool to
handle bot parameters.

"""
import argparse
from ConfigParser import SafeConfigParser


class IniFileConfiguration(object):
    "Basic Configuration class. Loads a .ini file "
    def __init__(self):
        # the only mandatory arguments
        default_vars = {
            'port': '6667',
            'nick': 'cmdbot',
            'ident': 'cmdbot',
            'realname': 'Cmd Bot',
            'admins': '',
        }
        parser = argparse.ArgumentParser("CmdBot")
        parser.add_argument('ini_file',
            help='path to the ini file to extract configuration from')
        args = parser.parse_args()

        config = SafeConfigParser()
        config.read(args.ini_file)

        self.host = config.get('general', 'host')
        self.chan = str(config.get('general', 'chan'))

        self.port = int(config.get('general', 'port', vars=default_vars))
        self.nick = config.get('general', 'nick', vars=default_vars)
        self.ident = config.get('general', 'ident', vars=default_vars)
        self.realname = config.get('general', 'realname', vars=default_vars)
        self.admins = config.get('general', 'admins', vars=default_vars).split()
