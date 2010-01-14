import os.path

from envbuilder.sh import sh

class WorkingDirPlaceholder(object):
    pass

class CustomCommand(object):
    def __init__(self, section, name):
        self._section = section
        self._name = name

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
                    cmd_text = default
            cwd = self._section['working_dir']
            # Single $ here since this will have already been run
            # through string interpolation
            cwd = cwd.replace('$PARCEL_WD', os.path.abspath(parcel.name))
            sh(cmd_text, cwd = cwd)
            
    def add_args(self, subparsers):
        parser = subparsers.add_parser(self._name, help=self._section['help'])
        parser.set_defaults(func=self.run)
