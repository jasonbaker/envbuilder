from envbuilder.sh import sh

class Update(object):
    def run(self, args, config):
        config.run_command('update')

    def add_args(self, subparsers):
        parser = subparsers.add_parser('update',
                                       help='Update checked out parcels')

        parser.set_defaults(func=self.run)
