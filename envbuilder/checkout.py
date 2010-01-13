from envbuilder.sh import sh

class Checkout(object):
    def run(self, args, config):
        for parcel in config.parcels:
            cmd = parcel['checkout']
            sh(cmd)
            
