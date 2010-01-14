import subprocess
from os import environ
from os.path import dirname, abspath, join

from configobj import ConfigObj
from validate import Validator
from pkg_resources import resource_filename

from envbuilder.sh import sh

configspec = resource_filename(__name__, 'configspec')

class Config(object):
    _config = None
    _val = None
    def __init__(self, filepath=None, config=None, name=None, args=None):
        assert (filepath or config), "Either filepath or config must be specified!"
        if not config:
            self._config = ConfigObj(filepath, unrepr=True,
                                     interpolation='Template',
                                     configspec=configspec)
            self._config.update(environ)
            self._val = Validator()
            self._config.validate(self._val)
        else:
            self._config = config
            self.name = name

        self.args = args

    def __getitem__(self, name):
        return self._config[name]

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)

    def _get_python(self):
        return abspath(self._config['project']['python'])

    def _raw(self):
        return self._config

    def run_command(self, cmd, cwd=None, parcels=None):
        """
        Run a command on all parcels.  The argument cmd specifies the
        config option name of the command, and cwd is the working
        directory to run the command from within.  If cwd is not
        specified or None, it will be the name of the parcel.
        """
        if parcels is None:
            parcels = self.parcels
        failed = []
        for parcel in parcels:
            run_steps = parcel[cmd]
            if not isinstance(run_steps, (tuple, list)):
                run_steps = [run_steps]
            try:
                for step in run_steps:

                    if cwd is None:
                        sh(step, join('.', parcel['name']))
                    else:
                        sh(step, cwd)
            except subprocess.CalledProcessError:
                failed.append(parcel['name'])
        return failed

    def select_parcels(self, parcel_names):
        """
        Return a subset of parcels with names in parcel_names.
        """
        return [parcel for parcel in self.parcels if parcel.name
                in parcel_names]
    
    @property
    def parcel_names(self):
        if self.args:
            return self.args.parcels.split(',')
        else:
            return self._config['project']['parcels']
        
    @property
    def parcels(self):
        parcel_names = self.parcel_names
        project = self._config['project']
        if not isinstance(parcel_names, (list, tuple)):
            parcel_names = [parcel_names]
        for parcel_name in parcel_names:
            if parcel_name.upper() != 'DEFAULT':
                yield Config(config=project[parcel_name], name=parcel_name)
        
class ConfigSection(object):
    _section = None
    def __init__(self, section):
        self._section = section
    def __getattr__(self, name):
        return self._section[name]
