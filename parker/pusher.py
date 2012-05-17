from inspect import getmembers

from parker.events import BaseEvent
from parker.loader import ParkerLoader

#TODO: move this to a template
WIDGET_CODE = """ <div id={widget_id}></div>
<script>
marimo.add_widget({
  widget_prototype: '{prototype}',
  id: '{widget_id}',
  template: '{template}',
  socket_path: '{socket}',
  queues: '{queues}'
});
</script>
"""


class BasePusher(object):

    #: the default template for this pusher's widgets
    default_template = None

    #: the queues this pusher's widgets should list on. TODO connect these with the events
    queues = []

    #: the socket path that the widgets should listen on
    socket = None

    #: the default prototype for this widget
    default_prototype = 'browsermq'

    # The following code may not belong here
    def collect_events(self):
        """ return all event instances associates with this pusher """
        return getmembers(self, lambda x: isinstance(x, BaseEvent))

    def setup_events(self):
        """ this really seems wrong 
            Do whatever the events think they need to get connected
            I'm also not sure how to get the queus if they're not static
        """
        for event in self.collect_events:
            event.connect()


    def get_template(self, template=None):
        """ just enough to work on the template tag """
        return ParkerLoader().get_template_source(template or self.default_template)

    def get_widget(self, widget_id, prototype=None, template=None, queues=None):
        """ once the templatetag finds this pusher this is all it should have call """
        context = dict(widget_id=widget_id,
                       prototype=prototype or self.default_prototype,
                       template = self.get_template(template),
                       queues = queues or self.queues,
                       )
        return WIDGET_CODE.format(context)


