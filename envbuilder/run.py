import sys
import os.path

from envbuilder.config import Config
from envbuilder.checkout import Checkout
from envbuilder.setup import Setup
from envbuilder.test import Test
from envbuilder.update import Update
from envbuilder.clean_pyc import CleanPyc
from envbuilder.custom import CustomCommand
from envbuilder.args import get_arg_parser

commands = [Checkout(),
            Setup(),
            Test(),
            Update(),
            CleanPyc()
            ]

def main():
    cwd = os.path.abspath(os.path.curdir)
    filepath = os.path.join(cwd, '.env')
    parser = get_arg_parser()
    if not os.path.isfile(filepath):
        sys.stderr.write('ERROR: This directory does not contain a .env file '
                         'or the .env file is a directory.\n')
        sys.exit(1)
    config = Config(filepath)

    subparsers = parser.add_subparsers()
    for command in commands:
        command.add_args(subparsers)
    command_section = config['commands']
    for command_name in command_section.sections:
        if command_name != 'DEFAULT':
            CustomCommand(section=command_section[command_name],
                          name=command_name).add_args(subparsers)
    args = parser.parse_args()
    config.args = args
    # args.func will have been set based on which command is
    # chosen
    args.func(args=args, config=config)

    
