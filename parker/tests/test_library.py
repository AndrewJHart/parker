from parker.library import ParkerLibrary

from mock import Mock

class TestLib(object):

    def test_register_object(self):
        pl = ParkerLibrary()
        mcarrier = Mock()
        mcarrier.return_value = 'instance?'
        mcarrier.name = 'test_name'
        pl.register(mcarrier)
        assert pl.carriers['test_name'] == 'instance?'

    def test_getitem(self):
        pl = ParkerLibrary()
        mcarrier = Mock()
        mcarrier.return_value = 'instance?'
        mcarrier.name = 'test_name'
        pl.register(mcarrier)
        assert pl['test_name'] == 'instance?'
