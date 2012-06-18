""" parker.listeners
=======================

Listeners connect to an event with their `setup` method and create a message via `get_message`.


"""


from django.http import HttpRequest
from parker.util import smartimport, LazyDescriptor


class BaseListener(object):
    """ All listeners much descend from this so they can be discovered by their carriers.
    They
    """
    def setup(self, publish):
        """ when a carrier is setting itself up it will call this.
        :param publish: The publish method of the carrier. This should take a message argument as well as *args and **kwargs to determine routing.
        """
        pass


class ModelListener(BaseListener):
    """ this  is a listener for model signals it defaults to post_save
        it either needs to have get_message overrriden or one can be passed in when it's created
    """

    signal = LazyDescriptor('signal')
    model = LazyDescriptor('model')


    def __init__(self, model, signal='django.db.models.signals.post_save', get_message=None):
        """
            :param model: the model or a string that this should listen to
            :param signal: the signal or a string to be imported later that this should connect to
            :get_message: TODO: fix this

        """
        self.signal = signal
        self.model = model
        if get_message:
            self.get_message = get_message

    def get_message(self, *args, **kwargs):
        """ this can be overriden or passed into __init__ for now """
        raise NotImplemented

    def setup(self, publish):
        """ ModelListener uses django signals of the model and connects publish to those """
        def handler(*args, **kwargs):
            message = self.get_message(*args, **kwargs)
            return publish(message, *args, **kwargs)

        self.signal.connect(handler, sender=self.model)

class TastyPieListener(ModelListener):
    """ Sets up a model listener using a tastypie resource to determin model and generate the message. """

    #: The resource that this listener will use.
    resource = LazyDescriptor("resource")

    @property
    def model(self):
        """ Get the model from the resource. """
        return self.resource._meta.queryset.model

    def __init__(self, resource, signal="django.db.models.signals.post_save"):
        """
            :param resource: A resource object or path to one that this listener should use.
            :param signal: The django signal of the model that this Listener is useing. defaults to `post_save`.
        """
        self.resource = resource
        self.signal = signal


    def process_message(self, message, sender, instance, **kwargs):
        """ TODO: this should either be used or deleted """
        return message

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
