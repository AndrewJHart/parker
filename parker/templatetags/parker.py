from django import template

from parker import parker_lib

register = template.Library()

@register.simple_tag('parker')
def parker_tag(pusher, widget_id, prototype=None, template=None, queues=None):
    return parker_lib['pusher'].get_widget(widget_id, prototype, template, queues)
