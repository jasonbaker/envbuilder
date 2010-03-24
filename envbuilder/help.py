import sys

from envbuilder.command import BuiltinCommand, Command
from envbuilder.custom import _CustomCommand
from envbuilder.args import Arguments
from envbuilder.sh import output_packages

class Help(BuiltinCommand):
    """
    Get help.
    """
    name = 'help'
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
            self.print_main_help()
        sys.exit(0)

    def print_main_help(self):
        print "SYNTAX:  envb [command]"
        output_packages(Command.builtin_cmd_mapping, 'Common commands')
        
        print '\nFor more info type "envb help <command>"'

    def print_help(self):
        args = sys.argv[1:]
        args.append('help')
        next_cmd = ' '.join(args)
        print "Run envbuilder %s for more info." % next_cmd
