import sys
import os.path

import pysistence

from envbuilder.command import BuiltinCommand
from envbuilder.template import PercentTemplater
from envbuilder.sh import sh
from envbuilder.util import classproperty

class WorkingDirPlaceholder(object):
    pass

def make_custom_command(section, name, aliases):
    class CommandFromEnv(_CustomCommand):
        names = [name] + aliases
        _name = name
        _section = section
        __doc__ = section['help']

        @classproperty
        def brief_help(cls):
            output_txt = cls.__doc__
            return output_txt + ' (from .env)'
        

class _CustomCommand(BuiltinCommand):
    """
    A custom command defined in the .env file.
    """
    _custom_cmd = {}
    @classproperty
    def custom_cmd_mapping(cls):
        return pysistence.make_dict(cls._custom_cmd)
    
    def run(self, args, config):
        for parcel in config.parcels:
            cmd_text = parcel.get(self._name)
            if cmd_text is None:
                default = self._section.get('default')
                if not default:
                    msg = "Parcel %s doesn't have required option %s" % (
                        parcel.name,
                        self._name)

                    assert not self._section['required'], msg
                    continue
                else:
                    cmd_text = self._percent_escape(parcel, default)
            cwd = self._section['working_dir']
            cwd = self._percent_escape(parcel, cwd)
            # NOTE:  deprecated
            # Single $ here since this will have already been run
            # through string interpolation
            cwd = cwd.replace('$PARCEL_WD', os.path.abspath(parcel['dir']))
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

    # For custom commands, we must give an instance.  Therefore, this is an
    # instance property.
    @classproperty
    def brief_help(self):
        return 'foo'
