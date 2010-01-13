import subprocess

def sh(cmd, cwd='.'):
    print '-->', cmd
    if cwd != '.':
        print '(%s)' % cwd
    # Eliminate empties
    cmd_list = [x for x in cmd.split() if x]
    subprocess.check_call(cmd_list, cwd=cwd)
