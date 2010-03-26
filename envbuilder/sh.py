import subprocess, sys, shlex, os
import textwrap

from envbuilder.terminal import TerminalController

term = TerminalController()

BINDIR = os.path.join(os.getcwd(), 'bin')

def sh(cmd, cwd='.'):
    """
    Execute command *cmd* from within directory *cwd*.
    """
    cmd = cmd.format(BINDIR=BINDIR)
    cwd = os.path.abspath(cwd)
    notify(cmd)
    notify('(From: %s)' % cwd, level=1)
    try:
        # So we can pass in an empty string to do nothing
        if cmd:
            subprocess.check_call(args=cmd, cwd=cwd, shell=True)
    except subprocess.CalledProcessError, e:
        cmd = e.cmd
        returncode = e.returncode
        notify('"%s" returned code %s' % (cmd, returncode))
        notify('ABORTED')
        sys.exit(returncode)

def notify(cmd, level=0):
    prompt = _generate_prompt(level)
    print term.BLUE + prompt  + cmd + term.NORMAL

def _generate_prompt(level):
    if level == 0:
        return '> '
    else:
        prompt = '> '
        for i in xrange(level):
            prompt = '-' + prompt
        return prompt
    

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

    
