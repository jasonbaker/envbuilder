import sys

from envbuilder.command import BuiltinCommand, Command
from envbuilder.args import Arguments

class Help(BuiltinCommand):
    names = ['help']

    def run(self, *args, **kwargs):
        # This method should never be called.  We are assuming that
        # parse_args will get called and will exit the program
        raise NotImplementedError

    def parse_args(self, raw_args):
        if len(raw_args) >= 1:
            secondary_command_name = raw_args[0]
            secondary_command_cls = Command.lookup_command(secondary_command_name)
            secondary_command = secondary_command_cls()
            secondary_command.print_help()
        else:
            self.print_base_help()
        sys.exit(0)

    def print_base_help(self):
        print "Placeholder"
