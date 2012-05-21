from inspect import getmembers

from django.template import Template, Context

from parker.events import BaseEvent
from parker.loader import ParkerLoader

#TODO: move this to a template
#TODO: making this a django template may have been a poor decision
WIDGET_CODE = """ <div id={{ widget_id }}></div>
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

    #: the queues this carrier's widgets should list on. TODO connect these with the events
    queues = []

    #: the socket path that the widgets should listen on
    socket = None

    #: the default prototype for this widget
    default_prototype = 'browsermq'

    def __init__(self):
        self.setup_events()

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
        return ParkerLoader().load_template_source(template or self.default_template)[0].replace('\n','')

    def get_widget(self, widget_id, prototype=None, template=None, queues=None):
        """ once the templatetag finds this carrier this is all it should have call """
        context = dict(widget_id=widget_id,
                       prototype=prototype or self.default_prototype,
                       template = self.get_template(template),
                       queues = queues or self.queues,
                       socket = self.socket
                       )
        template = Template(WIDGET_CODE)
        return template.render(Context(context))
