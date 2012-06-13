from parker.carrier import BaseCarrier
from parker.listeners import TastyPieListener

from parker.library import parker_lib

@parker_lib.register
class DemoCarrier(BaseCarrier):
    name = 'DemoCarrier'
    default_template = 'demo.html'
    queues = ['test.queue1']
    socket = 'mordechai.cei.cox.com:8000'

    demo_update = TastyPieListener('parker_demo.demo.resources.DemoResource')
