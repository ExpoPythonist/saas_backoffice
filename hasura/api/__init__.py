import json
import requests
from django.conf import settings


class Hasura:
    domain = settings.HASURA_URL
    url = None

    def __init__(self):
        try:
            import requests
        except ImportError:
            raise ImportError('\'requests\' package is required for this module, try running "pip install requests"')
        self.url = self.domain + '/v1/query'

    def _request(self, url, method, data, headers):
        method = getattr(requests, str(method).lower())
        response = method(url=url, data=json.dumps(data), headers=headers)
        return response.json()

    def request(self, method='POST', data=None, headers=None):
        return self._request(self.url, method, data, headers)
