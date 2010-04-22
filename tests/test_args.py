from envbuilder.args import Arguments

def test_get_command():
    # Remember: sys.argv[0] is the program name
    args = Arguments(['foo', 'bar'])
    actual_command = args.command
    expected_command = 'bar'
    assert actual_command == expected_command

def test_get_empty_command():
    args = Arguments([])
    actual_command = args.command
    expected_command = 'help'
    assert actual_command == expected_command

def test_get_arguments():
    args = Arguments(['foo', 'bar'])
    actual_args = args.arguments
    expected_args = ['bar']
    assert actual_args == expected_args

def test_get_empty_arguments():
    args = Arguments([])
    actual_args = args.arguments
    expected_args = []
    assert actual_args == expected_args
