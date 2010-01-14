import os.path

from envbuilder.config import Config
from envbuilder.checkout import Checkout
from envbuilder.setup import Setup
from envbuilder.test import Test
from envbuilder.update import Update
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
    args = parser.parse_args()
    args.func(args=args, config=config)

    
