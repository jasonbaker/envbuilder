import sys

import argparse

import envbuilder

class Arguments(object):
    def __init__(self, args=None):
        if args is None:
            try:
                args = sys.argv[1:]
            except IndexError:
                args = []
        self.args = args
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('command', default='help',
                                 help='The command to run',
                                 nargs='?',)
        self.parser.add_argument('--version', action='version',
                            version=envbuilder.__version__,
                            help='Get the version number and quit')
        options, remaining = self.parser.parse_known_args(self.args)
        self.command = options.command
        self.arguments = remaining
