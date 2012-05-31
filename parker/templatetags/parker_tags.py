import django
if django.VERSION < (1, 4, 0):
    from simple_tag.base_template import Library
else:
    from django.template import Library


from parker.library import parker_lib

register = Library()

@register.simple_tag(name='parker')
def parker_tag(carrier, widget_id, prototype=None, template=None, queues=None, initialize=False):
    return parker_lib[carrier].get_widget(widget_id, prototype, template, queues, initialize)
