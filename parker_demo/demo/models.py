from django.db import models
from django.dispatch import receiver

from parker.message import publish

class ParkerDemo(models.Model):
    title = models.CharField(max_length=140)
    summary = models.TextField(max_length=1000)
    link = models.CharField(max_length=1000)

# this is going here for now. The whole point of parker
# is to not have to write this type of code. But first
# it's useful to see what it would like if you had to write it
@receiver(models.signals.post_save, sender=ParkerDemo)
def publish_demo(sender, instance, **kwargs):
    message = dict(title=instance.title, summary=instance.summary, url=instance.link)
    publish('test.queue1', message)
