import os.path

from envbuilder.sh import sh

class Setup(object):
    """
    The class that runs the 'setup' command.
    """
    def run(self, args, config):
        if not args.no_create:
            sh('virtualenv --no-site-packages --clear .')
            requirements = config['project']['requires']
            easy_install = config['project']['easy_install'] 
            sh('%s pip' % easy_install)
            for requirement in requirements:
                sh('%s %s' % (easy_install, requirement))
                
        for parcel in config.parcels:
            build_cmds = parcel['setup']
            if not isinstance(build_cmds, (list, tuple)):
                build_cmds = [build_cmds]
            for build_cmd in build_cmds:
                sh(build_cmd, cwd=os.path.abspath(parcel['name']))

    def add_args(self, subparsers):
        parser = subparsers.add_parser('setup',
                                       help='Create a virtualenv and '
                                       'add parcels to it.')
        parser.add_argument('-n', '--no-create', default=False,
                            action='store_true',
                            help="Don't (re)create the virtualenv")
        parser.set_defaults(func=self.run)
