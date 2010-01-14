import subprocess, sys
from argparse import ArgumentParser

class Test(object):
    def run(self, args, config):
        if args.parcels:
            parcels = config.select_parcels(args.parcels.split(','))
        else:
            parcels = config.parcels

        failed = config.run_command('test', parcels=parcels)
        if failed:
            print '%s parcels had failing tests:' % len(failed)
            print '================='
            for item in failed:
                print item
            sys.exit(1)
        else:
            print 'All tests passing.'

    def add_args(self, subparsers):
        parser = subparsers.add_parser('test', help='Run tests.')
        parser.set_defaults(func=self.run)
        
