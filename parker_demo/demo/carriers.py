from random import randint

from parker.carrier import BaseCarrier
from parker.listeners import TastyPieListener

from parker.library import parker_lib






@parker_lib.register
class DemoCarrier(BaseCarrier):
    name = 'DemoCarrier'
    default_template = 'demo.html'
    queues = ['test.queue1']

    demo_update = TastyPieListener('parker_demo.demo.resources.DemoResource')

@parker_lib.register
class LoadCarrier(BaseCarrier):
    name = "LoadCarrier"

    default_template = 'load.html'


    queue_number = 100
    listen_concurrency = 10
    publish_concurrency = 10

    def get_queues(self, conc):
        return [str(randint(0,self.queue_count)) for _ in range(conc)]

    def get_publish_queues(self, *args, **kwargs):
        return self.get_queues(self.publish_concurrency)

    def get_listen_queues(self, *args, **kwargs):
        return self.get_queues(self.listen_concurrency)

    def test_publish(self, message=None):
        message = dict(message=message or str(randint(0,10000)))
        self.publish(message)
