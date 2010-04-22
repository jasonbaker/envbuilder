import envbuilder
from envbuilder.command import BuiltinCommand

class Version(BuiltinCommand):
    """
    Display the version of envbuilder and exit.
    """
    name = 'version'
    def run(self, args, config):
        print envbuilder.__version__
