from parker.events import BaseEvent, SignalEvent

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
