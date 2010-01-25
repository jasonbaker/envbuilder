import subprocess, sys

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
        subprocess.check_call(cmd_list, cwd=cwd)
    except subprocess.CalledProcessError, e:
        cmd = ' '.join(e.cmd)
        returncode = e.returncode
        notify('"%s" returned code %s' % (cmd, returncode))
        notify('ABORTED')
        sys.exit(returncode)

def notify(cmd):
    print '-->', cmd
        
