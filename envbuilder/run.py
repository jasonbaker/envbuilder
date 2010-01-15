import os.path

from envbuilder.config import Config
from envbuilder.checkout import Checkout
from envbuilder.setup import Setup
from envbuilder.test import Test
from envbuilder.update import Update
from envbuilder.custom import CustomCommand
from envbuilder.args import get_arg_parser

commands = [Checkout(),
            Setup(),
            Test(),
            Update(),
            ]

def main():
    cwd = os.path.abspath(os.path.curdir)
    filepath = os.path.join(cwd, '.env')
    config = Config(filepath)
    parser = get_arg_parser()
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
    args.func(args=args, config=config)

    
