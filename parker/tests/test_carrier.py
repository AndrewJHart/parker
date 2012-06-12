from parker.carrier import BaseCarrier
from parker.events import BaseEvent

from unittest2 import TestCase

from mock import patch, Mock, call

class TestBaseCarrier(TestCase):
    def setUp(self):
        class TestCarrier(BaseCarrier):
            default_queues = ['queue1','queue2']

        self.TestCarrier = TestCarrier
        self.carrier = TestCarrier()

    def test_collect_events(self):
        mock_conn = Mock()
        class TestEvent(object):
            handler = Mock()
            connect = mock_conn
            def connect(self, publish):
                pass

        event_instance1 = TestEvent()
        event_instance2 = TestEvent()

        class TestCarrier(BaseCarrier):
            def __init__(self):
                pass

            event1 = event_instance1
            event2 = event_instance2

        with patch('parker.carrier.BaseEvent', TestEvent):
            carrier = TestCarrier()
            self.assertTrue(event_instance1 in carrier.collect_events())
            self.assertTrue(event_instance2 in carrier.collect_events())


    def test_get_publish_queues(self):
        self.assertEqual(self.carrier.get_publish_queues(), ['queue1','queue2'])

    def test_get_subscribe_queues(self):
        self.assertEqual(self.carrier.get_subscribe_queues(), ['queue1','queue2'])

    @patch('parker.carrier.publish')
    def test_publish(self, pub):
        self.carrier.publish("message", "q")
        self.assertEqual(pub.call_count, 2)


    @patch('parker.carrier.BaseEvent')
    def test_setup_events(self, BE):
        event1 = Mock()
        event2 = Mock()
        self.carrier.collect_events = lambda : [event1, event2]
        self.carrier.setup_events()
        self.assertEqual(event1.connect.call_args, call(self.carrier.publish))
        self.assertEqual(event2.connect.call_args, call(self.carrier.publish))


class TestGetWidget(TestCase):

    class TestCarrier(BaseCarrier):
        default_prototype = "defproto"
        default_queues = ["defqueue"]
        socket = 'sock'

        def get_template(self, template=None):
            return "{{test}}"

        def get_context(self, queues, **kwargs):
            return dict(test="test1")

    def test_defaults(self):
        carrier = self.TestCarrier()
        with patch('parker.carrier.Template') as MTemplate:
            mock_template = Mock()
            MTemplate.return_value = mock_template
            carrier.get_widget('test_id')
            render_dict = mock_template.render.call_args[0][0]
            self.assertEqual(render_dict['queues'] , ['defqueue'])
            self.assertEqual(render_dict['prototype'] , 'defproto')
            self.assertEqual(render_dict['socket'] , 'sock')
            self.assertFalse('initial_state' in render_dict)


    def test_nondefaults(self):
        carrier = self.TestCarrier()
        with patch('parker.carrier.Template') as MTemplate:
            mock_template = Mock()
            MTemplate.return_value = mock_template
            carrier.get_widget('test_id', 'tproto', queues=['tqueue'])
            render_dict = mock_template.render.call_args[0][0]
            self.assertEqual(render_dict['queues'] , ['tqueue'])
            self.assertEqual(render_dict['prototype'] , 'tproto')
            self.assertFalse('initial_state' in render_dict)


    def test_initialize(self):
        carrier = self.TestCarrier()
        with patch('parker.carrier.Template') as MTemplate:
            mock_template = Mock()
            MTemplate.return_value = mock_template
            carrier.get_widget('test_id', initialize=True)
            render_dict = mock_template.render.call_args[0][0]
            self.assertEqual(render_dict['initial_state'], 'test1')
