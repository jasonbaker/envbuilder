from envbuilder.args import Arguments

def test_get_command():
    args = Arguments(['foo', 'bar'])
    actual_command = args.command
    expected_command = 'foo'
    assert actual_command == expected_command

def test_get_empty_command():
    args = Arguments([])
    actual_command = args.command
    expected_command = ''
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
