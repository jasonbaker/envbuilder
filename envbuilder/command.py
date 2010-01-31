import sys

import argparse

class Command(object):
    """
    An abstract base class for commands.
    """
    _cmd_mapping = {}

    @classmethod
    def lookup_command(cls, name):
        """
        This looks up a command by looking in two places:

          * The builtin command set
          * sys.modules

        So for instance, 'setup' would return the built in setup command,
        while 'py.something' would produce an import statement equivalent
        to 'from py import something'.
        """
        if name in cls._cmd_mapping:
            return cls._cmd_mapping[name]
        else:
            try:
                components = name.split('.')
                if len(components) == 1:
                    mod = __import__(name, globals(), locals())
                    # This is a top-level import.  Roughly translates to:
                    # import module
                    return mod
                else:
                    # Importing from a module.  a.b.c roughly translates to:
                    # from a.b import c
                    mod_name = '.'.join(components[:-1])
                    mod = __import__(mod_name, globals(), locals(),
                                     [mod_name])
                    prev = mod
                    for component in components[1:]:
                        prev = getattr(prev, component)
                    return prev
            except ImportError:
                sys.stderr.write('Command "%s" not found' % name)
                sys.exit(1)

    def print_help(self):
        parser = self.get_arg_parser()
        parser.print_help()

    def get_base_arg_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--parcels',
                            help = 'Select parcels to run this command on.')
        return parser

    def get_arg_parser(self):
        """
        Method to be overridden in subclasses.  Returns an
        argparse.ArgumentParser.
        """
        return self.get_base_arg_parser()

    def parse_args(self, args):
        parser = self.get_arg_parser()
        return parser.parse_args(args=args)

class MetaCommand(type):
    def __new__(cls, name, bases, dict):
        new_cls = type.__new__(cls, name, bases, dict)
        for name in new_cls.names:
            Command._cmd_mapping[name] = new_cls
        return new_cls
            
class BuiltinCommand(Command):
    names = []
    __metaclass__ = MetaCommand
    

