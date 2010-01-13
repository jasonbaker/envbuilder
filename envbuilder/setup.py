import os.path

from envbuilder.sh import sh

class Setup(object):
    def run(self, args, config):
        for parcel in config.parcels:
            build_cmds = parcel['build']
            if not isinstance(build_cmds, (list, tuple)):
                build_cmds = [build_cmds]
            for build_cmd in build_cmds:
                sh(build_cmd, cwd=os.path.abspath(parcel['name']))
        
