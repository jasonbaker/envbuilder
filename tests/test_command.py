import sys

import envbuilder
from envbuilder.command import BuiltinCommand, Command

def test_lookup_builtin():
    class SomeCommand(BuiltinCommand):
        name = 'some_command'

    command = Command.lookup_command('some_command')
    assert command is SomeCommand

def test_lookup_from_toplevel():
    class MyCommand(Command):
        pass
    sys.modules['my_command'] = MyCommand
    try:
        command = Command.lookup_command('my_command')
        assert command is MyCommand
    finally:
        del sys.modules['my_command']

def test_import_dot_qualified():
    # Using MyCommand2 just in case something didn't get cleaned up in
    # previous tests.
    class MyCommand2(Command):
        pass
    envbuilder.my_command2 = MyCommand2
    try:
        command = Command.lookup_command('envbuilder.my_command2')
        assert command is MyCommand2
    finally:
        del envbuilder.my_command2
