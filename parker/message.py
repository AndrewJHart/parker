""" this is a temporary place to hold the code needed to send messaged """
from kombu import Connection, Exchange

from django.conf import settings

# TODO multiple exhcanges
exchange = Exchange('browsermq_global', type='topic')

DEFAULT_BROKER_URL = "amqp://guest:guest@localhost:5672//"

def publish(route, message):
    """ simply send a messate to a route.

    :param route: a route in the browsermq format right now just a routing_key
    :param message: a dictionary or list to be send as the message
    """
    # TODO attempt to reuse connections
    url = getattr(settings, "PARKER_BROKER_URL", DEFAULT_BROKER_URL)
    with Connection(url) as conn:
        producer = conn.Producer()
        producer.publish(message,
            exchange = exchange,
            routing_key = route,
            serializer="json")
