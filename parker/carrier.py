from inspect import getmembers
import pystache
from django.template import Template, Context
from django.template.defaultfilters import escapejs

from parker.listeners import BaseListener
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
    default_queues = ['#']

    #: the socket path that the widgets should listen on
    socket = None

    #: the default prototype for this widget
    default_prototype = 'browsermq'

    #: does this widget initialize by default
    initialize = False

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
            publish(message, queue)



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

    def get_context(self, queues, **kwargs):
        """if you want to prepopulate a widget this should generate the context"""
        pass
