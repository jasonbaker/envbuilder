import sys
import os.path

from envbuilder.config import Config
from envbuilder.command import Command
from envbuilder.custom import make_custom_command
from envbuilder.args import Arguments

def main():
    cwd = os.path.abspath(os.path.curdir)
    filepath = os.path.join(cwd, '.env')
    if not os.path.isfile(filepath):
        sys.stderr.write('ERROR: This directory does not contain a .env file '
                         'or the .env file is a directory.\n')
        sys.exit(1)

    # reads sys.argv
    args = Arguments()

    config = Config(filepath)
    command_section = config['commands']
    for command_name in command_section.sections:
        if command_name != 'DEFAULT':
            make_custom_command(section=command_section[command_name],
                          name=command_name)
    command_cls = Command.lookup_command(args.command)
    command = command_cls()
    # hack - We need config to get the command, but we also need command
    # to get args.  Thus, we attach the args attribute after instantiation
    config.args = command.parse_args(args.arguments)
    command.run(config.args, config)


    
