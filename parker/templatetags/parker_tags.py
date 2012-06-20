"""parker.templatetags.parker_tags.
The parker template tag exists to get a widget for a carrier and put it in the page

.. autofunction:: parker.templatetags.parker_tags.parker_tag


Example
_________

.. literalinclude:: ../../parker_demo/templates/page1.html
"""



import django
if django.VERSION < (1, 4, 0):
    from simple_tag.base_template import Library
else:
    from django.template import Library


from parker.library import parker_lib

register = Library()

@register.simple_tag(name='parker')
def parker_tag(carrier, widget_id, prototype=None, template=None, queues=None, initialize=False):
    """ The parker tag looks in the carrier library and gets widget code from it.

    :param carrier: The name of the carrier this wisget should use.
    :param widget_id: The id this widget should have in marimo.
    :keyword prototype: The widget prototype to use.
    :keyword template: The mustache template to pass to the widget.
    :keyword queues: The queues this widget should subscribe to.
    :keyword initialize: Should this widget initialize itself.

    All keywords default to the values of the carrier.
    """
    return parker_lib[carrier].get_widget(widget_id, prototype, template, queues, initialize)
