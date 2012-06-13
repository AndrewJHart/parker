from parker.listeners import BaseListener, ModelListener

from mock import patch, Mock


class TestModelListener(object):
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
