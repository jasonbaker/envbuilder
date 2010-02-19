import subprocess, sys, copy
from os import environ, getcwd
from os.path import dirname, abspath, join

from configobj import ConfigObj, Section
from validate import Validator
from pkg_resources import resource_filename

from envbuilder.sh import sh, terminate, notify

configspec = resource_filename(__name__, 'configspec')

class Config(object):
    _config = None
    _val = None
    def __init__(self, filepath=None, config=None, name=None, args=None):
        assert (filepath or config), "Either filepath or config must be specified!"
        self.args = args

        if not config:
            self._config = self.assemble_configobj(filepath)
        else:
            self._config = config
            self.name = name
            self._config['name'] = self.name

        self._config['CWD'] = getcwd()




        if hasattr(self._config, 'validate'):
            self._val = Validator()
            self._config.validate(self._val)



    def assemble_configobj(self, filepath):
        non_interpolating_config = self.new_configobj(filepath,
                                                      configspec=configspec,
                                                      unrepr=True)
        config = self.new_configobj(filepath,
                                    unrepr=True,
                                    interpolation='Template',
                                    configspec=configspec)
        others = non_interpolating_config['also']
        if not isinstance(others, (list, tuple)):
            others = [others]
        for other_path in others:
            other_cfg = self.new_configobj(other_path,
                                           unrepr=True,
                                           interpolation='Template',
                                           configspec=configspec)
            config.merge(other_cfg)
        return config

    def new_configobj(self, *args, **kwargs):
        config = ConfigObj(*args, **kwargs)
        config['CWD'] = getcwd()
        environ_dict = copy.copy(environ)
        for key, value in environ_dict.iteritems():
            if isinstance(value, str):
                environ_dict[key] = value.replace('$', '$$')
        config.update(environ_dict)
        config.walk(self.name_parcels, call_on_sections=True)
        return config
        

    def name_parcels(self, section, key):
        val = section[key]
        if not isinstance(val, Section):
            return
        val['name'] = key

    def __getitem__(self, name):
        return self._config[name]

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)

    def run_command(self, cmd, cwd=None, parcels=None, required=True):
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
            try:
                run_steps = parcel[cmd]
            except KeyError, e:
                if required:
                    msg_template = 'Section "%s" missing required option %s'
                    terminate(msg_template % (parcel['name'], cmd))
                else:
                    notify('Skipping %s' % parcel['name'])
                    continue
                
            if not isinstance(run_steps, (tuple, list)):
                run_steps = [run_steps]
            try:
                for step in run_steps:
                    if step:
                        if cwd is None:
                            sh(step, join('.', parcel['dir']))
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
        if self.args.parcels:
            return self.args.parcels.split(',')
        else:
            return self._config['project']['parcels']

    @property
    def parcel_dirs(self):
        project_section = self._config['project']
        for name in self.parcel_names:
            yield project_section[name]['dir']
            
    @property
    def parcels(self):
        parcel_names = self.parcel_names
        project = self._config['project']
        if not isinstance(parcel_names, (list, tuple)):
            parcel_names = [parcel_names]
        for parcel_name in parcel_names:
            if parcel_name.upper() != 'DEFAULT':
                yield Config(config=project[parcel_name], name=parcel_name)


    
