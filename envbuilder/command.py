import sys, textwrap

import argparse, pysistence, pkg_resources

import envbuilder
from envbuilder.util import classproperty
from envbuilder.sh import sh, notify

class Command(object):
    """
    An abstract base class for commands.
    """
    _cmd_mapping = {}
    py_dependencies=[]
    @classproperty
    def builtin_cmd_mapping(cls):
        """
        A mapping of the built-in commands.
        """
        return pysistence.make_dict(cls._cmd_mapping)

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
        if not name:
            name = 'help'
        
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
                sys.stderr.write('Command "%s" not found\n\n' % name)
                sys.exit(1)

    def print_help(self):
        """
        Print out the full help message.  By default, this calls
        the print_help method on the parser returned by
        :meth:`~envbuilder.command.Command.get_arg_parser`.
        """
        print self.brief_help
        parser = self.get_arg_parser()
        parser.print_help()

    def get_base_arg_parser(self):
        """
        This returns the argument parser with the base functionality.
        This should not be overridden in subclasses unless you know
        what you are doing.
        """
        parser = argparse.ArgumentParser(prog='envb %s' % self.name,
                                         fromfile_prefix_chars='@')
        parser.add_argument('-p', '--parcels',
                            help = 'Select parcels to run this command on.')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            default=True,
                            help='Print verbose errors.')
        parser.add_argument('-N', '--no-deps',
                            default=False, action='store_true',
                            help="Don't automatically install a command's dependencies")
        parser.add_argument('-U', '--upgrade',
                            default=False, action='store_true',
                            help="Update dependencies")
        return parser

    def get_arg_parser(self):
        """
        Method to be overridden in subclasses.  Returns an
        :class:`argparse.ArgumentParser`.  By default, this
        returns the same as
        :meth:`~envbuilder.command.Command.get_base_arg_parser`.

        In general, this method should get its parser from
        :meth:`~envbuilder.command.Command.get_base_arg_parser`.
        Otherwise, some command-line options might not work.
        """
        return self.get_base_arg_parser()

    def parse_args(self, args):
        parser = self.get_arg_parser()
        return parser.parse_args(args=args)

    @classproperty
    def brief_help(cls):
        return cls.__doc__

    def run(self, args, config):
        """
        Stub class to be overridden in subclasses.  This is
        where the actual logic of the command should go.
        """
        raise NotImplementedError

    def main(self, args, config):
        """
        This is the function to call to run a command.  This
        does handling of various tasks such as installing
        dependencies.
        """
        if not args.no_deps:
            self.handle_dependencies(args)
        self.run(args, config)

    def handle_dependencies(self, args):
        """
        Install any python dependencies that are not findable by
        pkg_resources.require.
        """
        for dependency in self.py_dependencies:
            try:
                pkg_resources.require(dependency)
            except pkg_resources.DistributionNotFound:
                notify('Installing %s' % dependency)
                sh("pip install '%s'" % dependency)
            except pkg_resources.VersionConflict:
                notify('Upgrading %s' % dependency)
                sh("pip install -U '%s'" % dependency)

class MetaCommand(type):
    def __new__(cls, name, bases, dict):
        new_cls = type.__new__(cls, name, bases, dict)
        if not new_cls.no_use and name != 'BuiltinCommand':
            Command._cmd_mapping[new_cls.name] = new_cls
            for name in new_cls.aliases:
                Command._cmd_mapping[name] = new_cls
        return new_cls
            
class BuiltinCommand(Command):
    name = ''
    aliases = []
    no_use = False
    __metaclass__ = MetaCommand
    

