from inspect import getmembers
import pystache
from django.template import Template, Context
from django.template.defaultfilters import escapejs

from parker.events import BaseEvent
from parker.loader import ParkerLoader
from parker.message import publish

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

    #: the default template for this carrier's widgets
    default_template = None

    #: for now each carrier will publish to it's own exchange
    exchange = None

    #: the default exchange type is topic exchange
    exchange_type = 'topic'

    #: this only works for topic exchanges. otherwise consider changing it
    default_queue = '#'

    #: the socket path that the widgets should listen on
    socket = None

    #: the default prototype for this widget
    default_prototype = 'browsermq'

    #: does this widget initialize by default
    initialize = False

    def __init__(self):
        self.setup_events()

    def publish(self, message, queue):
        publish(q, message)

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
    def collect_events(self):
        """ return all event instances associates with this carrier """
        return [x[1] for x in getmembers(self, lambda x: isinstance(x, BaseEvent))]

    def setup_events(self):
        """ this really seems wrong 
            Do whatever the events think they need to get connected
            I'm also not sure how to get the queus if they're not static
        """
        for event in self.collect_events():
            event.connect()

    def get_template(self, template=None):
        """ just enough to work on the template tag """
        #TODO what should we do about multiline templates here
        return ParkerLoader().load_template_source(template or self.default_template)[0]

    def get_widget(self, widget_id, prototype=None, template=None, queues=None, initialize=None, **kwargs):
        """ once the templatetag finds this carrier this is all it should have call """
        mustache_template = self.get_template(template)
        context = dict(widget_id=widget_id,
                       prototype=prototype or self.default_prototype,
                       template = escapejs(mustache_template),
                       queues = queues or self.subscribe_queues(**kwargs),
                       socket = self.socket
                       )
        if initialize is None:
            initialize = self.initialize
        if initialize:
            initial_context = self.get_context(**kwargs)
            if initial_context:
                context['initial_state'] = pystache.render(mustache_template, self.get_context(context['queues'],**kwargs))
        template = Template(WIDGET_CODE)
        return template.render(Context(context))

    def get_context(self, queues, **kwargs):
        """if you want to prepopulate a widget this should generate the context"""
        for queue in 
