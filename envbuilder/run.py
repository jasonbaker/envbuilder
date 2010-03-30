import sys
import os.path

from envbuilder.config import Config
from envbuilder.command import Command
from envbuilder.custom import make_custom_command
from envbuilder.args import Arguments
from envbuilder.sh import notify

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
    handle_command_path(config)
    command_section = config['commands']
    for command_name in command_section.sections:
        if command_name != 'DEFAULT':
            section=command_section[command_name]
            make_custom_command(section=section,
                                cmd_name=command_name,
                                cmd_aliases=section['aliases'])
    command_cls = Command.lookup_command(args.command)
    command = command_cls()
    # hack - We need config to get the command, but we also need command
    # to get args.  Thus, we attach the args attribute after instantiation
    config.args = command.parse_args(args.arguments)
    command.main(config.args, config)

def handle_command_path(config):
    for path in config['project']['command-path']:
        sys.path.append(path)
    try:
        import builtins
    except ImportError, i:
        notify('WARNING:  unable to find builtin commands')
