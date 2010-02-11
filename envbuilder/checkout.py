import sys

from envbuilder.sh import sh
from envbuilder.command import BuiltinCommand

class Checkout(BuiltinCommand):
    """
    Checkout all parcels.
    """
    names = ['checkout', 'co']
    def run(self, args, config):
        config.run_command('checkout', cwd='.')

            
    def add_args(self, subparsers):
        parser = subparsers.add_parser('checkout', help='Check out parcels.')
        parser.set_defaults(func=self.run)

