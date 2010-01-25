import subprocess

def sh(cmd, cwd='.'):
    """
    A somewhat easier interface to subprocess.check_call.
    """
    print '-->', cmd
    if cwd != '.':
        print '(From: %s)' % cwd
    # Eliminate empties
    cmd_list = [x for x in cmd.split() if x]
    subprocess.check_call(cmd_list, cwd=cwd)
