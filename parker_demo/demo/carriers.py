from parker.carriers import BaseCarrier
from parker.listeners import TastyPieListener

from parker.library import parker_lib


@parker_lib.register
class DemoCarrier(BaseCarrier):
    """ a simple demo carrier using a single tastypie listener """

    # the name this carrier can be found at in the registry
    name = 'DemoCarrier'
    # the default mustache template to use
    default_template = 'demo.html'
    # the default queues to publish to and listen on
    queues = ['test.queue1']

    # A single listener to publish messages
    demo_update = TastyPieListener('parker_demo.demo.resources.DemoResource')
