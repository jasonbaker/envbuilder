import sys
import os.path

import pysistence

from envbuilder.command import BuiltinCommand
from envbuilder.template import PercentTemplater
from envbuilder.sh import sh
from envbuilder.util import classproperty

class WorkingDirPlaceholder(object):
    pass

def make_custom_command(section, cmd_name, cmd_aliases):
    class CommandFromEnv(_CustomCommand):
        no_use = False
        name = cmd_name
        aliases = cmd_aliases
        _section = section
        __doc__ = section['help']

        __init__ = BuiltinCommand.__init__

        @classproperty
        def brief_help(cls):
            output_txt = cls.__doc__
            return output_txt + ' (from .env)'
        

class _CustomCommand(BuiltinCommand):
    """
    A custom command defined in the .env file.
    """
    no_use = True
    _custom_cmd = {}
    def __init__(self, *args, **kwargs):
        # The user should *never* see this.  This class wasn't meant to be
        # instantiated.
        raise NotImplementedError

    @classproperty
    def custom_cmd_mapping(cls):
        return pysistence.make_dict(cls._custom_cmd)
    
    def run(self, args, config):
        for parcel in config.parcels:
            cmd_text_list = parcel.get(self.name)
            if cmd_text_list is None:
                default = self._section.get('default')
                if not default:
                    msg = "Parcel %s doesn't have required option %s" % (
                        parcel.name,
                        self.name)

                    assert not self._section['required'], msg
                    continue
                else:
                    cmd_text_list = [self._percent_escape(parcel, cmd)
                                     for cmd in default]
            elif not isinstance(cmd_text_list, list):
                cmd_text_list = [cmd_text_list]
            cwd = self._section['working_dir']
            cwd = self._percent_escape(parcel, cwd)
            # NOTE:  deprecated
            # Single $ here since this will have already been run
            # through string interpolation
            cwd = cwd.replace('$PARCEL_WD', os.path.abspath(parcel['dir']))
            for cmd_text in cmd_text_list:
                sh(cmd_text, cwd = cwd)

    def _percent_escape(self, parcel, text):
        templater = PercentTemplater(text)
        text = templater.substitute(parcel)
        return text
            
    def add_args(self, subparsers):
        parser = subparsers.add_parser(self._name, help=self._section['help'])
        parser.set_defaults(func=self.run)

    def print_help(self):
        print self._section['help']

    @classproperty
    def brief_help(cls):
        return cls._section['help']
