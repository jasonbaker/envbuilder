import subprocess, sys
import textwrap

def sh(cmd, cwd='.'):
    """
    A somewhat easier interface to subprocess.check_call.
    """
    notify(cmd)
    if cwd != '.':
        print '(From: %s)' % cwd
    # Eliminate empties
    cmd_list = [x for x in cmd.split() if x]
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
    print '-->', cmd
        
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

    
