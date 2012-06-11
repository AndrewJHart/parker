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


class Listener(object):
    def __init__(self, signal, model):
        self._signal = signal
        self._model = model

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
