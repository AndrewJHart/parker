from tastypie.resources import ModelResource
from parker_demo.demo.models import ParkerDemo

class DemoResource(ModelResource):
    class Meta:
        queryset = ParkerDemo.objects.all()
        resource_name =  'demo'
