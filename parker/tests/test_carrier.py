from parker.carrier import BaseCarrier

from unittest2 import TestCase

from mock import patch, Mock

class TestBaseCarrier(TestCase):
    def setUp(self):
        class TestCarrier(BaseCarrier):
            pass
        self.TestCarrier = TestCarrier

    def test_collect_events(self):
        mock_conn = Mock()
        class TestEvent(object):
            connect = mock_conn

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
            carrier.setup_events()
            self.assertEqual(mock_conn.call_count, 2)
