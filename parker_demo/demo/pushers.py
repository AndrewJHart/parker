""" and example for what "pusher" might look like to guide their development for now
    this is similiar to a tastypie resource and should at some point be able to be generated from them
    I'm still not exactly sure how they connected can they server multiple models? do they have to import anything?

    A problem this doesn't solve but needs to is that widgets should get what they want to listen to out of this somehow
    perhaps just the meta queues for a list of pushers.  perhaps there should be an overridable helper that can be passed arguments
"""

from parker import pusher
from parker.events import model_event
from parker.fields import TextField, IntegerField


class ParkerDemoPusher(pusher.Pusher):
    class Meta:
        events = [model_event('parker_demo.models.ParkerDemo', 'post_save'),]
        queues = ['test.queue1', ]

    # if this wasn't defined it would just use the queues from meta
    def queues(self, instance):
       queues = self._meta.queues
       queues.append(instance.app_label + instance.id)
       return ['test.queue1',]

    title = TextField(attribute='title')
    summary = TextField(attribute='summary')
    id = IntegerField(attribute='id')
    url = TextField(attribute='link')

    def clean_url(self, instance, data):
        if not data:
            data = instance.get_absolute_url()
        return data
