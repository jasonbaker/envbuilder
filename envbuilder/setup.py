import os.path

from envbuilder.sh import sh
from envbuilder.checkout import Checkout

class Setup(object):
    def run(self, args, config):
        for parcel in config.parcels:
            build_cmd = parcel['build']
            sh(build_cmd, cwd=os.path.abspath(parcel.name))
        
