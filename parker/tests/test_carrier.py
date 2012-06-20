from parker.carriers import BaseCarrier, CachingCarrier
from unittest2 import TestCase

from mock import patch, Mock, call

class TestBaseCarrier(TestCase):
    def setUp(self):
        class TestCarrier(BaseCarrier):
            default_queues = ['queue1','queue2']

        self.TestCarrier = TestCarrier
        self.carrier = TestCarrier()

    def test_collect_listeners(self):
        mock_conn = Mock()
        class TestListener(object):
            handler = Mock()
            connect = mock_conn
            def connect(self, publish):
                pass

        listener_instance1 = TestListener()
        listener_instance2 = TestListener()

        class TestCarrier(BaseCarrier):
            def __init__(self):
                pass

            listener1 = listener_instance1
            listener2 = listener_instance2

        with patch('parker.carriers.BaseListener', TestListener):
            carrier = TestCarrier()
            self.assertTrue(listener_instance1 in carrier.collect_listeners())
            self.assertTrue(listener_instance2 in carrier.collect_listeners())


    def test_get_publish_queues(self):
        self.assertEqual(self.carrier.get_publish_queues(), ['queue1','queue2'])

    def test_get_subscribe_queues(self):
        self.assertEqual(self.carrier.get_subscribe_queues(), ['queue1','queue2'])

    @patch('parker.carriers.publish')
    def test_publish(self, pub):
        self.carrier.publish("message", "q")
        self.assertEqual(pub.call_count, 2)

    @patch('parker.carriers.publish')
    def test_publish_none(self, pub):
        self.carrier.publish(None)
        self.assertFalse(pub.called)

    @patch('parker.carriers.BaseListener')
    def test_setup_listeners(self, BE):
        listener1 = Mock()
        listener2 = Mock()
        self.carrier.collect_listeners = lambda : [listener1, listener2]
        self.carrier.setup_listeners()
        self.assertEqual(listener1.setup.call_args, call(self.carrier.publish))
        self.assertEqual(listener2.setup.call_args, call(self.carrier.publish))

    def test_get_context_default(self):
        self.assertEqual(BaseCarrier().get_context(), {})

    def test_get_context(self):
        bc = BaseCarrier()
        ctx = dict(a=1, b=2)
        bc.default_context = ctx
        self.assertEqual(bc.get_context(), bc.default_context)

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
        with patch('parker.carriers.Template') as MTemplate:
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
        with patch('parker.carriers.Template') as MTemplate:
            mock_template = Mock()
            MTemplate.return_value = mock_template
            carrier.get_widget('test_id', 'tproto', queues=['tqueue'])
            render_dict = mock_template.render.call_args[0][0]
            self.assertEqual(render_dict['queues'] , ['tqueue'])
            self.assertEqual(render_dict['prototype'] , 'tproto')
            self.assertFalse('initial_state' in render_dict)


    def test_initialize(self):
        carrier = self.TestCarrier()
        with patch('parker.carriers.Template') as MTemplate:
            mock_template = Mock()
            MTemplate.return_value = mock_template
            carrier.get_widget('test_id', initialize=True)
            render_dict = mock_template.render.call_args[0][0]
            self.assertEqual(render_dict['initial_state'], 'test1')


class TestCachingCarrier(TestCase):
    def setUp(self):
        self.carrier = CachingCarrier()
        self.carrier.default_queues = ['queue1', 'queue2']

    @patch('parker.carriers.cache')
    @patch('parker.carriers.time')
    @patch('parker.carriers.publish')
    def test_publish(self, publish, time, cache):
        time.time.return_value = 100
        self.carrier.publish('message')
        cache.set.assert_called_any('queue1', (100, 'message'))
        cache.set.assert_called_any('queue2', (100, 'message'))
        self.assertEqual(cache.set.call_count, 2)

    @patch('parker.carriers.cache')
    @patch('parker.carriers.publish')
    def test_publish_none(self, pub, cache):
        self.carrier.publish(None)
        self.assertFalse(pub.called)
        self.assertFalse(cache.set.called)

    @patch('parker.carriers.cache')
    def test_get_context(self, cache):
        cdict = {}
        for q, t in zip(self.carrier.default_queues, range(2)):
            cdict[self.carrier.cache_key % q] = (t, q)
        cache.get = lambda x: cdict[x]

        context = self.carrier.get_context(self.carrier.default_queues)
        self.assertEqual(context, 'queue2')
