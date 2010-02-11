import os.path, sys

from envbuilder.sh import sh
from envbuilder.command import BuiltinCommand

class Setup(BuiltinCommand):
    """
    Set up the parcels.  This usually installs the parcel into 
    the virtualenv.
    """
    names = [ 'setup' ]
    def run(self, args, config):
        if not args.no_create:
            venv_opts = config['project']['virtualenv-args']
            sh('virtualenv ' + venv_opts)
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

    def get_arg_parser(self):
        parser = self.get_base_arg_parser()
        parser.add_argument('-n', '--no-create', default=False,
                            action='store_true',
                            help="Don't (re)create the virtualenv")
        parser.add_argument('-U', '--upgrade', default=False,
                            action='store_true',
                            help='Upgrade requirements listed in the .env file')
        return parser

