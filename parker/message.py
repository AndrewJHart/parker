""" this is a temporary place to hold the code needed to send messaged """
from kombu import Connection, Exchange


#TODO don't hard code these
QUEUE_URL = "amqp://guest:guest@localhost:5672//"
exchange = Exchange('browsermq_global', type='topic')

def publish(route, message):
    """ simply send a messate to a route.

    :param route: a route in the browsermq format right now just a routing_key
    :param message: a dictionary or list to be send as the message
    """
    # TODO don't hardcode this and attempt to reuse connections
    with Connection("amqp://guest:guest@localhost:5672//") as conn:
        producer = conn.Producer()
        #TODO I think I need to dump this to keep from pickling and sending a stream
        producer.publish(message,
            exchange = exchange,
            routing_key = route,
            serializer="json")
