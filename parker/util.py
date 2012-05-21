
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
