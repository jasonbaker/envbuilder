
import pdb
import os

class CleanPyc(object):
    def run(self, args, config):
        clean_pyc (config.parcel_dirs)

    def add_args(self, subparsers):
        parser = subparsers.add_parser('clean_pyc',
                        help='Delete all .pyc files in project subdirectories')
        parser.set_defaults(func=self.run)


def clean_pyc(paths):
    "Delete all .pyc files in path and recursively within its subdirectories."
    print 'Deleting all .pyc files in project subdirectories'
    target_paths = []
    for path in paths:
        assert os.path.isdir(path), '%s is not a directory' % path
        target_paths +=  gather_directories_recursively(path)
    for path in target_paths:
        filenames = os.listdir(path)
        killfiles = [os.path.join(path,filename) for filename in filenames
                     if filename.endswith('.pyc')]
        for kf in killfiles:
            print 'Deleting file',kf
            os.remove(kf)


def gather_directories_recursively (fpath):
    pathList = []
    def append_dirs (junk, dirpath, nameList):
        for name in nameList:
            fullpath = os.path.join(dirpath,name)
            # We don't want to look at non-directory files right now
            # Also, don't delete files from the virtualenv lib directory
            if os.path.isdir(fullpath) and 'python2.6' not in fullpath:
                pathList.append (fullpath)
    os.path.walk(fpath, append_dirs, None)
    return pathList
