import subprocess

def sh(cmd, cwd='.'):
    print cmd
    cmd_list = cmd.split()
    subprocess.check_call(cmd_list, cwd=cwd)
