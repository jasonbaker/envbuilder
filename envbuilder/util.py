class classproperty(object):
    """
    A property that may be defined on a class.

    This comes from Alex Martelli:

    http://stackoverflow.com/questions/2173206/is-there-any-way-to-create-a-class-property-in-python/2173321#2173321
    """
    def __init__(self, f):
        self.f = classmethod(f)
    def __get__(self, *a):
            return self.f.__get__(*a)()
