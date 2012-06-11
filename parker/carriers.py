from functools import partial

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
