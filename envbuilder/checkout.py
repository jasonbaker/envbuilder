from envbuilder.sh import sh

class Checkout(object):
    def run(self, args, config):
        for parcel in config.parcels:
            cmd = parcel['checkout']
            sh(cmd)
            
    def add_args(self, subparsers):
        parser = subparsers.add_parser('checkout', help='Check out parcels.')
        parser.set_defaults(func=self.run)
