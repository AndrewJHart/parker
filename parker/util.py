
def smartimport(mpath):
    """ Given a path smart_import will import the module and return the attr reffered to """
    # TODO this should raise proper ImportErrors when it fails
    parts = mpath.split('.')
    try:
        mod = __import__(mpath)
    except ImportError:
        mod = smartimport('.'.join(parts[:-1]))
        mod = getattr(mod, parts[-1])
    else:
        for p in parts[1:]:
            mod = getattr(mod, p)
    return mod


def load_carrier(carrier_name):
    """ this works for now but should probably be changes """
    CClass = smartimport(carrier_name)
    return CClass()



class LazyDescriptor(object):
    """ this uses smartimport to turn a string into what it's supposed to be when it's accessed """

    def __init__(self, name, *args):
        """ this requires a name where it will eventually store the data and optionally an initial value
        """
        if args:
            self.val = args[0]
        self.name = "_" + name

    def __get__(self, obj, cls):
        if not hasattr(obj, self.name):
            if hasattr(self, 'val'):
              setattr(obj, self.name, self.val)
            else:
                raise AttributeError

        if isinstance(getattr(obj, self.name), basestring):
            setattr(obj, self.name, smartimport(getattr(obj, self.name)))

        return getattr(obj, self.name)


    def __set__(self, obj, val):
        setattr(obj, self.name, val)
