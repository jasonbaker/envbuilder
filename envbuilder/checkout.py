import envbuilder.vcs as vcs

class Checkout(object):
    def run(self, args, config):
        for parcel in config.parcels:
            vcs_module = getattr(vcs, parcel['vcs'])
            vcs_obj = vcs_module.VCS()
            vcs_obj.checkout(parcel['url'], parcel.name)
            
