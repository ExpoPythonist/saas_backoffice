from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from hasura.roles import HasuraRoles
from hasura.utils import AuthResponse


class HasuraWebHookAuth(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)

    def handle_auth(self):
        user = self.request.user
        user_role = HasuraRoles.ANONYMOUS
        if user.is_authenticated:
            user_role = HasuraRoles.USER
            if user.is_staff:
                user_role = HasuraRoles.ADMIN
            resp = AuthResponse(user_id=user.id, role=user_role)
        else:
            resp = AuthResponse(role=user_role)
            resp.status_code = status.HTTP_401_UNAUTHORIZED
        return resp

    def post(self, request):
        return self.handle_auth()

    def get(self, request):
        return self.handle_auth()
