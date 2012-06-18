from parker.listeners import BaseListener, ModelListener

from mock import patch, Mock


class TestModelListener(object):

    def test_is_base(self):
        assert issubclass(ModelListener, BaseListener)

    def test_setup(self):
        model = Mock()
        signal = Mock()
        get_message= Mock()
        ml = ModelListener(model, signal, get_message)
        publish = Mock()
        ml.setup(publish)
        assert not publish.called
        assert not get_message.called
        assert signal.connect.called
        handler = signal.connect.call_args[0][0]
        handler()
        assert publish.called
        assert get_message.called

    def test_get_message(self):
        model = Mock()
        model.a = 1
        model.b = 2
        model.c = 3
        ml = ModelListener(model, fields=['a','b'])
        mess = ml.get_message(model)
        assert mess['a'] == 1
        assert mess['b'] == 2
        assert not 'c' in mess
