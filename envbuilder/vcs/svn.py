import subprocess

from envbuilder.sh import sh


class VCS(object):
    def checkout(self, url, dirname):
        sh('svn co %s %s' % (url, dirname))
