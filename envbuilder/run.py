import os.path

from envbuilder.config import Config
from envbuilder.checkout import Checkout
from envbuilder.setup import Setup
from envbuilder.test import Test
from envbuilder.args import get_args

commands = { 'checkout' : Checkout,
             'co' : Checkout,
             'setup' : Setup,
             'test' : Test,
             }

def main():
    cwd = os.path.abspath(os.path.curdir)
    filepath = os.path.join(cwd, '.env')
    config = Config(filepath)
    cmd_args = get_args()
    command = commands[cmd_args.command]()
    command.run(args=cmd_args, config=config)
    
