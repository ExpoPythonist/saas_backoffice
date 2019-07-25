from django.http import JsonResponse


class AuthResponse(JsonResponse):
    data = {}

    def __init__(self, user_id=None, role=None, custom=None):
        """Custom is a dictionary value of field that should be returned,
        for example {'name': 'User-of-app'} is translated to {'X-Hasura-name': 'User-of-app'}"""
        if custom is None:
            custom = dict()
        custom.update({'User-Id': user_id, 'Role': role})
        self.populate_data_from_custom_fields(**custom)
        super(AuthResponse, self).__init__(data=self.data)

    def populate_data_from_custom_fields(self, **kwargs):
        for key in kwargs.keys():
            val = str(kwargs.get(key))
            if isinstance(key, bool):
                val = val.lower()
            self.data.update({f'X-Hasura-{key}': val})
