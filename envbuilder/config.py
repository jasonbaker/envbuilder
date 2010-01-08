from os.path import dirname, abspath, join

from configobj import ConfigObj
from validate import Validator

this_directory = abspath(dirname(__file__))
configspec = join(this_directory, 'configspec')

class Config(object):
    _config = None
    _val = None
    def __init__(self, filepath):
        self._config = ConfigObj(filepath, unrepr=True, interpolation='Template',
                                 configspec=configspec)
        # self._val = Validator()
        # success = self._config.validate(self._val)
        # assert success

    def __getattr__(self, name):
        return ConfigSection(self._config[name])

    def _get_python(self):
        return abspath(self._config['project']['python'])

    def _raw(self):
        return self._config
                               
        
class ConfigSection(object):
    _section = None
    def __init__(self, section):
        self._section = section
    def __getattr__(self, name):
        return self._section[name]
