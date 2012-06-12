from functools import partial

from parker.util import smartimport

class ModelSignalCarrier(object):
    def setup_listeners(self):
        for listener in self.collect_listeners:
            listener.connect(partial(self.handle_event, listener.get_message))

    def publish(self, message, queue):
        pass

    def handle_event(self, message_fxn, *args, **kwargs):
        message = message_fxn(*args, **kwargs)
        for queue in self.publish_queue(*args, **kwargs):
            self.publish(message, queue)

    def get_publish_queues(self, *args, **kwargs):
        return self.default_queue

    def get_subscribe(self, *args, **kwargs):
        return self.default_queues


class ModelListener(object):
    def __init__(self, model, signal='django.db.models.signals.post_save', get_message=None):
        self._signal = signal
        self._model = model
        if get_message:
            self.get_message = get_message

    @property
    def signal(self):
        if isinstance(self._signal, basestring):
            self._signal = smartimport(self._signal)
        return self._signal

    @property
    def model(self):
        if isinstance(self._model, basestring):
            self._model = smartimport(self._signal)
        return self._model

    def connect(self, fxn):
        self.signal.connect(fxn, sender=self.model)

    def get_message(self, *args, **kwargs):
        raise NotImplemented

class TastyPieListener(ModelListener):
    def __init__(self, resource, signal='django.db.models.signals.post_save'):
        self._resource = resource

    @property
    def resource(self):
        """ this really needs to be dried out """
        pass


    def get_message(self, *args, **kwargs):
        """ from tastypie handler """
        pass
