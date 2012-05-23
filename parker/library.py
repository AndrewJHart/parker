class ParkerLibrary(object):
    """ for now this just keeps a dictionary of carriers
        it should eventually deal with signals and stuff too
    """

    carriers = {}

    def register(self, carrier):
        """ should registration and connection be separate steps """
        self.carriers[carrier.name] = carrier()

    def __getitem__(self, key):
        return self.carriers[key]

# TODO move this a rename it
library = ParkerLibrary()
