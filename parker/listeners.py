""" parker.listeners
=======================

Listeners connect to an event with their `setup` method and create a message via `get_message`.

ModelListener
________________

.. autoclass:: ModelListener
    :members:


TastyPieListener
_________________

.. autoclass:: TastyPieListener
    :members:


Writing your own listener
____________________________
To write your own listener extent `BaseListener` and define a setup method.

.. autoclass::  BaseListener
    :members:

"""


from django.http import HttpRequest
from parker.util import LazyDescriptor


class BaseListener(object):
    """ All listeners much descend from this so they can be discovered by their carriers.
    The only thing a listener must define is a setup method which takes a publish function as it's only argument.
    The publish function expects to be called with a message, and arguments to determine what queues to send the message too

    """
    def setup(self, publish):
        """ when a carrier is setting itself up it will call this.

        :param publish: The publish method of the carrier. It should take a message argument and arguments to determine routing.
        """
        pass


class ModelListener(BaseListener):
    """
    The model listener connects to model signals.
    If your message is simple and includes only json serializable attributes on the model instance you can pass these in in the fields arg.

    If you need more complex messages or model attributes that aren't json serializable you will have to override the get_message method.
    """

    signal = LazyDescriptor('signal', 'django.db.models.signals.post_save')
    model = LazyDescriptor('model')


    def __init__(self, model, signal=None, fields=None):
        """
            :param model: the model or a string that this should listen to
            :keyword signal: the signal or a string to be imported later that this should connect to. default=post_save
            :keyword fields: The fields to include in the message. default=None

        """
        if signal is not None:
            self.signal = signal
        self.model = model
        self.fields = fields or []

    def get_message(self, instance, *args, **kwargs):
        """ returns a dict of the field lists for a  """
        return dict([(field, getattr(instance, field)) for field in self.fields])

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
