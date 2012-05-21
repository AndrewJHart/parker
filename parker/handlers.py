""" for now handlers will handle everything.
    much of this needs to come from the carrier itself.
"""
from parker.message import publish


class Handler(object):
    def __call__(self, **kwargs):
        publish(self.get_queues(**kwargs), self.get_message(**kwargs))

    def get_queues(self, **kwargs):
        """ this determines what queues a message goes too """
        raise NotImplemented

    def get_message(self, **kwargs):
        """ this determines the object that will be seriealized into the message """
        raise NotImplemented

class ModelHandler(Handler):

    def __init__(self, queues, fields=None):
        self.queues = queues
        self.fields = fields

    def get_queues(self, **kwargs):
        return self.queues

    def get_message(self, sender, **kwargs):
        fields = self.fields or [x.name for x in sender._meta.fields]
        return  dict([[field, getattr(sender, field)] for field in fields])
