import subprocess, sys, copy, traceback
from os import environ, getcwd
from os.path import dirname, abspath, join

try:
    from configobj import ConfigObj, Section, MissingInterpolationOption
    from validate import Validator
except ImportError:
    pass

from pkg_resources import resource_filename, require

from envbuilder.sh import sh, terminate, notify

configspec = resource_filename(__name__, 'configspec')

class Config(object):
    """
    This represents the actual .env file.
    """
    _config = None
    _val = None
    def __init__(self, filepath=None, config=None, name=None, args=None):
        # We don't want to ensure that configobj is loaded until we
        # actually want to use it
        require('configobj')
        self.filepath = filepath
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
        others = non_interpolating_config.get('also', [])
        if not isinstance(others, (list, tuple)):
            others = [others]
        for other_path in others:
            other_cfg = self.new_configobj(other_path,
                                           unrepr=True,
                                           interpolation='Template',
                                           configspec=configspec)
            try:
                config.merge(other_cfg)
            except MissingInterpolationOption, e:
                self._handle_missing_interp(e, other_path)
        return config

    def _handle_missing_interp(self, e, path=None):
        if self.args and self.args.verbose:
            traceback.print_exc()
        else:
            notify(str(e))
        if path:
            terminate('While merging file %s' % path)
        else:
            terminate('File unknown')


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
        # Bypass interpolation.  ConfigObj 4.8.0 should include
        # functionality to make this a bit more clear.
        val = dict.__getitem__(section, key)
        if not isinstance(val, Section):
            return
        val['name'] = key

    def __getitem__(self, name):
        """
        Get the option or subsection named by :arg:`name`.
        """
        try:
            return self._config[name]
        except MissingInterpolationOption, e:
            self._handle_missing_interp(e, self.filepath)

    def get(self, *args, **kwargs):
        """
        Equivalent to dict.get.
        """
        return self._config.get(*args, **kwargs)

    def run_command(self, cmd, cwd=None, parcels=None, required=True):
        """
        Run a command on parcels selected from the command-line via the -p flag.
        The argument cmd specifies the config option name of the
        command, and cwd is the working directory to run the command
        from within.  If cwd is not specified or None, it will be the
        name of the parcel.
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
        """
        The names of parcels specified by the user via
        the -p flag.
        """
        if self.args.parcels:
            return self.args.parcels.split(',')
        else:
            return self._config['project']['parcels']

    @property
    def parcel_dirs(self):
        """
        The directories of all parcels specified by the user
        via the -p flag.
        """
        project_section = self._config['project']
        for name in self.parcel_names:
            yield project_section[name]['dir']
            
    @property
    def parcels(self):
        """
        The config sections representing all parcels specified
        by the user via the -p flag.
        """
        parcel_names = self.parcel_names
        project = self._config['project']
        if not isinstance(parcel_names, (list, tuple)):
            parcel_names = [parcel_names]
        for parcel_name in parcel_names:
            if parcel_name.upper() != 'DEFAULT':
                yield Config(config=project[parcel_name], name=parcel_name,
                             args=self.args)


    
