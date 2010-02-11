import sys

from envbuilder.sh import sh
from envbuilder.command import BuiltinCommand

class Checkout(BuiltinCommand):
    """
    Checkout all parcels.
    """
    name = 'checkout'
    aliases = ['co']
    def run(self, args, config):
        config.run_command('checkout', cwd='.')
