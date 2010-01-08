import envbuilder.vcs as vcs

class Checkout(object):
    def run(self, args, config):
        project = config.project
        subproject_names = project.repos
        if not isinstance(subproject_names, (list, tuple)):
            subproject_names = [subproject_names]
        for subproject_name in subproject_names:
            if subproject_name.lower() != 'DEFAULT':
                subproject = getattr(project, subproject_name)
                vcs_module = getattr(vcs, subproject['vcs'])
                vcs_obj = vcs_module.VCS()
                vcs_obj.checkout(subproject['url'], subproject_name)
            
