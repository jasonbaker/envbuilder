from envbuilder.sh import sh

class Update(object):
    def run(self, args, config):
        if args.parcels:
            parcels = config.select_parcels(args.parcels.split(','))
        else:
            parcels = config.parcels
        config.run_command('update', parcels=parcels)

    def add_args(self, subparsers):
        parser = subparsers.add_parser('update',
                                       help='Update checked out parcels')
        parser.add_argument('-p', '--parcels', default=None,
                            help='A comma-separated list of parcels to update.')
        parser.set_defaults(func=self.run)
