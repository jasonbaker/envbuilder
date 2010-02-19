from envbuilder.sh import sh
from envbuilder.command import BuiltinCommand

class Update(BuiltinCommand):
    """
    Updates parcels that have already been checked out.
    """
    name = 'update'
    aliases = ['up']
    def run(self, args, config):
        config.run_command('update', required=False)

    def add_args(self, subparsers):
        parser = subparsers.add_parser('update',
                                       help='Update checked out parcels')

        parser.set_defaults(func=self.run)
