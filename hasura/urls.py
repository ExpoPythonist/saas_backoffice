from django.urls import path

from hasura.auth import HasuraWebHookAuth

urlpatterns = [
    path('webhook/auth/', HasuraWebHookAuth.as_view(), name='auth-webhook'),
]
