
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

    #: val is what this attribute will get before it's set. It's `None` so that things which iterate over all attributes won't break on the class itself
    val = None

    def __init__(self, name, *args):
        """ this requires a name where it will eventually store the data and optionally an initial value
        """
        if args:
            self.val = args[0]
        self.name = "_" + name

    def __get__(self, obj, cls):
        # if obj is none this is class not an instance.
        # import and stick in self.val
        if obj is None:
            if isinstance(self.val, basestring):
                self.val = smartimport(self.val)
            return self.val

        # this is the first time we've gotten on this object move for self.val to object.name
        if not hasattr(obj, self.name):
              setattr(obj, self.name, self.val)

        if isinstance(getattr(obj, self.name), basestring):
            setattr(obj, self.name, smartimport(getattr(obj, self.name)))

        return getattr(obj, self.name)


    def __set__(self, obj, val):
        if obj is None:
            self.val = val
        else:
            setattr(obj, self.name, val)
