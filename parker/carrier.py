""" parker.carrier
======================

The carrier contains all of the information for one realtime widget. 
- It defines when information will be sent(listeners).
- What information will be sent(listenters).
- Where it will be sent to(get_publish_queues).
- What widget this will use(default_template).
- What that widget will listen too(get_subscribe_queues).

Listeners
___________
Instances of `parker.BaseListener` which are attributes of a carrier will be conncected. This is the primary method for publishing.

BaseCarrier
_____________
.. autoclass:: parker.carrier.BaseCarrier
    :members:


Examples
________
Here is a simple example carrier

.. literalinclude:: ../../parker_demo/demo/carriers.py

"""
import time
from inspect import getmembers
import pystache
from django.conf import settings
from django.core.cache import cache
from django.template import Template, Context
from django.template.defaultfilters import escapejs

from parker.listeners import BaseListener
from parker.loader import ParkerLoader
from parker.message import publish


DEFAULT_SOCKET = ''

#TODO: move this to a template
#TODO: making this a django template may have been a poor decision
WIDGET_CODE = """ <div id={{ widget_id }}>{{ initial_state|safe}}</div>
<script>
marimo.add_widget({
  widget_prototype: '{{ prototype }}',
  id: '{{ widget_id }}',
  template: '{{ template|safe }}',
  socket_path: '{{ socket }}',
  queues: {{ queues|safe }}
});
</script>
"""


class BaseCarrier(object):

    #: the default mustache template for this carrier's widgets
    default_template = None

    #: the default exchange type is topic exchange
    exchange_type = 'topic'

    #: queues defaults to all which is specific to topic exchanges.
    default_queues = ['#']

    #: where the widget will connect connect to browsermq
    @property
    def socket(self):
        return getattr(settings, 'PARKER_DEFAULT_SOCKET', DEFAULT_SOCKET)

    #: the default prototype for this widget
    default_prototype = 'browsermq'

    #: does this widget initialize by default
    initialize = False

    #: the default context to initialize with
    default_context = {}

    def __init__(self):
        self.setup_listeners()

    def get_publish_queues(self, *args, **kwargs):
        """ based on the arguments given to a signal what queues should it publish too
            default is the default_queues
        """
        return self.default_queues

    def get_subscribe_queues(self, *args, **kwargs):
        """ based on the arguments given to the template tag what queues should this listen on
            default is the default_queues
        """
        return self.default_queues

    # The following code may not belong here
    def collect_listeners(self):
        """ return all listener instances associates with this carrier """
        return [x[1] for x in getmembers(self, lambda x: isinstance(x, BaseListener))]

    def setup_listeners(self):
        """ this really seems wrong 
            Do whatever the listeners think they need to get connected
            I'm also not sure how to get the queus if they're not static
        """
        for listener in self.collect_listeners():
            listener.setup(self.publish)

    def publish(self, message, *args, **kwargs):
        for queue in self.get_publish_queues(*args, **kwargs):
            publish(queue, message)

    def get_template(self, template=None):
        """ just enough to work on the template tag """
        #TODO what should we do about multiline templates here
        return ParkerLoader().load_template_source(template or self.default_template)[0]

    def get_widget(self, widget_id, prototype=None, template=None, queues=None, initialize=None, **kwargs):
        """ once the templatetag finds this carrier this is all it should have call
        """
        mustache_template = self.get_template(template)
        context = dict(widget_id=widget_id,
                       prototype=prototype or self.default_prototype,
                       template = escapejs(mustache_template),
                       queues = queues or self.get_subscribe_queues(**kwargs),
                       socket = self.socket
                       )
        if initialize is None:
            initialize = self.initialize
        if initialize:
            initial_context = self.get_context(context['queues'], **kwargs)
            if initial_context:
                context['initial_state'] = pystache.render(mustache_template, initial_context)
        template = Template(WIDGET_CODE)
        return template.render(Context(context))

    def get_context(self, *args, **kwargs):
        """ return the default context. """
        return getattr(self, 'default_context')


class CachingCarrier(BaseCarrier):
    """ this carrier is set up for simple caching.
        on publish is saves the message for each queue it's listening to with a timestamp
        on widget creation it get's the cache for each queue and populates the widget with the newest one.
    """
    #: the cache to use after the queue name is subsituted in. This value will allow multiple carriers that publish to the same queue to overwrite each other.
    cache_key = 'parker:caching_carrier:%s'

    def publish(self, message, *args, **kwargs):
        for queue in self.get_publish_queues(*args, **kwargs):
            publish(queue, message)

            cache.set(self.cache_key % queue, (time.time(), message))

    def get_context(self, queues, **kwargs):
        """if you want to prepopulate a widget this should generate the context"""
        message = None
        for queue in queues:
            nmessage = cache.get(self.cache_key % queue)
            if message is None or nmessage[0] > message[0]:
                message = nmessage

        return message[1]
