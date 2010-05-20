import os.path, sys

from envbuilder.sh import sh, warn
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
        pip_cmd = self.get_pip_cmd(config, args)
        self.install_env_requires(config, pip_cmd)
        self.install_requirements_files(config, pip_cmd)
        config.run_command('setup', required=False)
        
    def get_arg_parser(self):
        parser = self.get_base_arg_parser()
        parser.add_argument('-n', '--no-create', default=False,
                            action='store_true',
                            help="Don't (re)create the virtualenv")
        return parser

    def install_env_requires(self, config, pip_cmd):
        required = config['project']['requires']
        if required:
            warn('The requires attribute is deprecated and will be removed in a '
                 'future release.')
        for requirement in required:
            sh('%s %s' % (pip_cmd, requirement))
 
    def get_pip_cmd(self, config, args):
        if args.upgrade:
            upgrade_flag = '-U'
        else:
            upgrade_flag = ''
        return 'pip install -E . %s' % upgrade_flag
 

    def install_requirements_files(self, config, pip_cmd):
        requirements_files = config['project']['requirements']
        for fname in requirements_files:
            if os.path.exists(fname):
                sh('%s -r %s' % (pip_cmd, fname))
            else:
                warn('Requirements file %s not found.  Skipping.' % fname)
