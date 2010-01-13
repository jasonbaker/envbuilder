from os import environ
from os.path import dirname, abspath, join

from configobj import ConfigObj
from validate import Validator

this_directory = abspath(dirname(__file__))
configspec = join(this_directory, 'configspec')

class Config(object):
    _config = None
    _val = None
    def __init__(self, filepath=None, config=None, name=None):
        assert (filepath or config), "Either filepath or config must be specified!"
        if not config:
            self._config = ConfigObj(filepath, unrepr=True,
                                     interpolation='Template',
                                     configspec=configspec)
            self.name = name
            self._val = Validator()
            self._config.validate(self._val)
        else:
            self._config = config


    def __getattr__(self, name):
        return ConfigSection(self._config[name])

    def __getitem__(self, name):
        return self._config[name]

    def _get_python(self):
        return abspath(self._config['project']['python'])

    def _raw(self):
        return self._config

    @property
    def parcels(self):
        project = self._config['project']
        parcel_names = project['parcels']
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
