from parker.events import BaseEvent, SignalEvent, ModelListener

from mock import patch, Mock

class TestSignalEvent(object):

    def test_is_baseevent(object):
        """ make sure we will be able to find this as an event """
        assert isinstance(SignalEvent(1,2,3), BaseEvent)

    @patch('parker.events.smartimport')
    def test_connect_noimport(self, mimport):
        msignal = Mock()
        event = SignalEvent(msignal, 2, 3)
        event.connect()
        assert not mimport.called
        assert msignal.connect.called

    @patch('parker.events.smartimport')
    def test_connect_import(self, mimport):
        msignal = Mock()
        mimport.return_value = msignal
        event = SignalEvent('msignal', 3)
        event.connect()
        assert mimport.called
        assert msignal.connect.called

class TestModelListener(object):
    def test_connect(self):
        model = Mock()
        signal = Mock()
        get_message= Mock()
        ml = ModelListener(model, signal, get_message)
        publish = Mock()
        ml.connect(publish)
        assert not publish.called
        assert not get_message.called
        assert signal.connect.called
        handler = signal.connect.call_args[0][0]
        handler()
        assert publish.called
        assert get_message.called
