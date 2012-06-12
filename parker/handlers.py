""" for now handlers will handle everything.
    much of this needs to come from the carrier itself.
"""
from django.http import HttpRequest
from parker.message import publish
from parker.util import smartimport

class Handler(object):
    default_queue = None

    def __call__(self, **kwargs):
        for q in self.get_queues(**kwargs):
            publish(q, self.get_message(**kwargs))

    def get_queues(self, **kwargs):
        """ this determines what queues a message goes too """
        return self.default_queue

    def get_message(self, **kwargs):
        """ this determines the object that will be seriealized into the message """
        raise NotImplemented

class ModelHandler(Handler):

    def __init__(self, queues, fields=None):
        self.queues = queues
        self.fields = fields

    def get_queues(self, **kwargs):
        return self.queues

    def get_message(self, sender, instance, **kwargs):
        fields = self.fields or [x.name for x in instance._meta.fields]
        return  dict([[field, getattr(instance, field)] for field in fields])


class TastyPieHandler(Handler):
    def __init__(self, queues, resource):
        self.queues = queues
        self.resource = resource

    def get_message(self, sender, instance, **kwargs):
        """ unfortunately the design of tastypie makes it hard to use it to just serialize objects
            if you do much with the request in your resource this will break
        """
        if isinstance(self.resource, basestring):
            self.resource = smartimport(self.resource)
        resource = self.resource()
        # is this the least disruptive way to to this?
        def get_obj(**kwargs):
            return instance
        self.resource.get_obj = get_obj
        # if anything tries to use this it will likely fail
        req = HttpRequest()
        bundle = resource.build_bundle(obj=instance)
        bundle = resource.full_dehydrate(bundle)
        # TODO: should we even support this? it seems likely to be request specific
        bundle = resource.alter_detail_data_to_serialize(req, bundle)
        return resource.serialize(req, bundle, 'application/json')
