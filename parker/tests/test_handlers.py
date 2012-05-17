from parker.handlers import ModelHandler

from mock import Mock


class TestModelHandler(object):
    def test_get_queues(self):
        handler = ModelHandler('testqueue')
        assert handler.get_queues() == 'testqueue'


    def test_get_models(object):
        sender = Mock()
        fields = dict(x=1, y=2, z=3)
        sender._meta.fields = []
        for f,v in fields.items():
            setattr(sender, f, v)
            field = Mock()
            field.name = f
            sender._meta.fields.append(field)
        handler = ModelHandler('testqueue')
        assert fields == handler.get_message(sender)
        fields.pop('z')
        handler= ModelHandler('testqueue', ['x','y'])
        assert fields == handler.get_message(sender)
