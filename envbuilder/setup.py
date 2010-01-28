import os.path

from envbuilder.sh import sh

class Setup(object):
    """
    The class that runs the 'setup' command.
    """
    def run(self, args, config):
        if not args.no_create:
            sh('virtualenv --no-site-packages --clear .')
        if args.upgrade:
            upgrade_flag = '-U'
        else:
            upgrade_flag = ''
        requirements = config['project']['requires']
        easy_install = config['project']['easy_install'] 
        for requirement in requirements:
            sh('%s %s %s' % (easy_install, upgrade_flag, requirement))
                
        for parcel in config.parcels:
            build_cmds = parcel['setup']
            if not isinstance(build_cmds, (list, tuple)):
                build_cmds = [build_cmds]
            for build_cmd in build_cmds:
                sh(build_cmd, cwd=os.path.abspath(parcel['dir']))

    def add_args(self, subparsers):
        parser = subparsers.add_parser('setup',
                                       help='Create a virtualenv and '
                                       'add parcels to it.')
        parser.add_argument('-n', '--no-create', default=False,
                            action='store_true',
                            help="Don't (re)create the virtualenv")
        parser.add_argument('-U', '--upgrade', default=False,
                            action='store_true',
                            help='Upgrade requirements listed in the .env file')
        parser.set_defaults(func=self.run)
