import subprocess

class Test(object):
    def run(self, args, config):
        try:
            config.run_command('test')
        except subprocess.CalledProcessError:
            print '================='
            print "TESTS FAILED"
            
