""" the events are used to connect """
from parker.util import smartimport


class BaseEvent(object):
    """ for now this just exists to check if an object is an event. 
       code may be moved up here later
    """
    pass

class SignalEvent(BaseEvent):
    """ this event is a django signal I assume this is going to be the main
        way of triggering events
    """

    def __init__(self, signal, handler, sender=None):
        # TODO these imports should maybe be delayed

        self.signal = signal
        self.handler = handler
        self.sender = sender

    def connect(self):
        if isinstance(self.signal, basestring):
            self.signal = smartimport(self.signal)
        if isinstance(self.handler, basestring):
            self.handler = smartimport(self.handler)
        if isinstance(self.sender, basestring):
            self.sender = smartimport(self.sender)
        if self.sender:
            self.signal.connect(self.handler, self.sender)
        else:
            self.signal.connect(self.handler)
