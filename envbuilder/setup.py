import os.path

from envbuilder.sh import sh
from envbuilder.checkout import Checkout

class Setup(object):
    def run(self, args, config):
        sh('virtualenv --no-site-packages .')
        co = Checkout()
        co.run(args, config)
        project = config.project
        subproject_names = config.project.repos
        if not isinstance(subproject_names, (list, tuple)):
            subproject_names = [subproject_names]
        for subproject_name in subproject_names:
            if subproject_name.lower() != 'default':
                subproject = getattr(project, subproject_name)
                build_cmd = config._raw()['project'][subproject_name]['build']
                sh(build_cmd, cwd=os.path.abspath(subproject_name))
        
