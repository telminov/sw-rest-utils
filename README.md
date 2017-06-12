# sw-rest-utils
REST helpers


## Declaration
for example in my_app/rest.py
```python
from django.conf import settings
from sw_rest_utils import BaseRest


class SomeResource(BaseRest):
    url = settings.OTHER_SERVICE_URL + '/rest/some_resource/'
    label = 'Super resource first'


class DynamicallyUrl(BaseRest):
    def __init__(self, pk):
        self.pk = pk

    def get_url(self):
        return settings.OTHER_SERVICE_URL + '/rest/some_resource/' + str(self.pk)


class ResourceWithGetParams(BaseRest):
    url = settings.OTHER_SERVICE_URL + '/rest/some_resource/'

    def __init__(self, some_filter_value):
        self.some_filter_value = some_filter_value

    def get_params(self):
        return {
            'some_filter_value': self.some_filter_value
        }


class ResourceWithPostParams(BaseRest):
    url = settings.OTHER_SERVICE_URL + '/rest/some_resource/'
    method = 'PUT'

    def __init__(self, some_value):
        self.some_value = some_value

    def get_data(self):
        return {
            'some_value': self.some_value
        }


class CustomResponseProcess(BaseRest):
    url = settings.OTHER_SERVICE_URL + '/rest/some_resource/'

    def process_request(self):
        result = super().process_request()
        result['total'] = result['foo'] + result['bar']
        return result


class CustomHeaders(BaseRest):
    def get_headers(self):
        return {'Authorization': 'Token {0}'.format(settings.AUTH_TOKEN)}

```

## Usage
for example in my_app/views.py
```python
from rest_framework.response import Response
import my_app.rest


def some_view(request):
    result = my_app.rest.SomeResource().process_request()
    value = result['some_response_value']
    return Response({'other_service_result': value})

```


For useing RestExceptionView add REST_EXCEPTION_PROCESSING flag at setings.py

```
...
REST_EXCEPTION_PROCESSING = True
...

```

And add view in urls.py

```
from sw_rest_utils.views import RestException
...
url(r'^rest_exception/$', RestException.as_view, {'template_name': 'app/my_template.html'}, name='rest_exception'),

...
```
