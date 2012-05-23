from django import template

from parker.library import parker_lib

register = template.Library()

@register.simple_tag(name='parker')
def parker_tag(carrier, widget_id, prototype=None, template=None, queues=None):
    return parker_lib[carrier].get_widget(widget_id, prototype, template, queues)