import subprocess, sys, shlex
import textwrap

from envbuilder.terminal import TerminalController

term = TerminalController()

def sh(cmd, cwd='.'):
    """
    A somewhat easier interface to subprocess.check_call.
    """
    notify(cmd)
    if cwd != '.':
        print '(From: %s)' % cwd
    cmd_list = shlex.split(cmd)
    try:
        # So we can pass in an empty string to do nothing
        if cmd:
            subprocess.check_call(cmd_list, cwd=cwd)
    except subprocess.CalledProcessError, e:
        cmd = ' '.join(e.cmd)
        returncode = e.returncode
        notify('"%s" returned code %s' % (cmd, returncode))
        notify('ABORTED')
        sys.exit(returncode)

def notify(cmd):
    print term.BLUE + '--> ' + cmd + term.NORMAL

def terminate(msg, returncode=1):
    """
    Notify the user of an error and end the program.
    """
    notify(msg)
    notify('ABORTED')
    sys.exit(returncode)

def output_packages(pkg_dict, name):
    """
    Print out a help string from a list of packages returned by
    Command.builtin_cmd_mapping.
    """
    print '%s:' % name
    for key in sorted(pkg_dict.iterkeys()):
        package = pkg_dict[key]
        # The user should *never* see this
        assert package.brief_help, '%s has an empty help string' % package
        help_text = textwrap.dedent(package.brief_help.strip('\n'))
        help_text = help_text.replace('\n', '')
        msg = '%s - %s' % (key, help_text)
        formatted_msg = textwrap.fill(msg,
                                      subsequent_indent = '   ',
                                      initial_indent=' * ')
        print formatted_msg

    
