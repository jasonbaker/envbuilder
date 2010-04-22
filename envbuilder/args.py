import sys

class Arguments(object):
    def __init__(self, args=sys.argv):
        self.args = args

    @property
    def command(self):
        try:
            return self.args[1]
        except IndexError:
            # This is an empty list, so return nothing.
            return 'help' 

    @property
    def arguments(self):
        try:
            return self.args[2:]
        except IndexError:
            # This is an empty list, so return an empty list
            return []
