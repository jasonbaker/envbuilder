import os.path, sys

from envbuilder.sh import sh
from envbuilder.command import BuiltinCommand

class Setup(BuiltinCommand):
    """
    Set up the parcels.  This usually installs the parcel into 
    the virtualenv.
    """
    name = 'setup'
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
                
        config.run_command('setup', required=False)
        
    def get_arg_parser(self):
        parser = self.get_base_arg_parser()
        parser.add_argument('-n', '--no-create', default=False,
                            action='store_true',
                            help="Don't (re)create the virtualenv")
        return parser

