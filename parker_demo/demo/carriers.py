from parker.carrier import BaseCarrier
from parker.events import SignalEvent
from parker.handlers import ModelHandler

class DemoCarrier(BaseCarrier):
    name = 'DemoCarrier'
    default_template = 'demo.html'
    queues = ['test.queue1']
    socket = 'mordechai.cei.cox.com:8000'

    demo_model_event = SignalEvent( 'django.db.models.signals.post_save',
                                     ModelHandler(['test_queue1']),
                                     'parker_demo.demo.models.ParkerDemo')
