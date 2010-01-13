import subprocess, sys

class Test(object):
    def run(self, args, config):
        failed = config.run_command('test')
        if failed:
            print '%s parcels had failing tests:' % len(failed)
            print '================='
            for item in failed:
                print item
            sys.exit(1)
        else:
            print 'All tests passing.'
